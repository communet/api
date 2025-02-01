from dataclasses import dataclass
from typing import Optional

from src.domain.entities.users import AuthData, Profile, Credentials
from src.domain.values.users import Password
from src.infra.converters.users import convert_profile_model_to_entity
from src.infra.repositories.users import UserUoW
from src.infra.services.jwt import BaseJWTService
from src.infra.services.redis import BaseRedisService
from src.logic.commands.base import BaseCommand, CommandHandler
from src.logic.exceptions.auth import InvalidCredentialsException, UnauthorizedException, UserAlreadyExistsException


@dataclass(frozen=True)
class RegisterCommand(BaseCommand):
    display_name: str
    username: str
    email: str
    password: str
    avatar: str


@dataclass(frozen=True)
class RegisterCommandHandler(CommandHandler[RegisterCommand, Profile]):
    user_uow: UserUoW

    async def handle(self, command: RegisterCommand) -> Profile:
        async with self.user_uow as uow:
            if await uow.credentials_repository.check_user_exists(email=command.email, username=command.username):
                raise UserAlreadyExistsException(email=command.email, username=command.username)

            credentials = Credentials.create(command.username, command.email, command.password)
            profile = Profile.create(command.display_name, command.avatar, credentials)

            await uow.credentials_repository.create(credentials)
            await uow.profile_repository.create(profile)

        return profile


@dataclass(frozen=True)
class LoginCommand(BaseCommand):
    username: Optional[str]
    email: Optional[str]
    password: str


@dataclass(frozen=True)
class LoginCommandHandler(CommandHandler[LoginCommand, AuthData]):
    jwt_service: BaseJWTService
    redis_service: BaseRedisService
    user_uow: UserUoW

    async def handle(self, command: LoginCommand) -> AuthData:
        async with self.user_uow as uow:
            creds = (
                await uow.credentials_repository.find_by_username(command.username)
                if command.username else
                await uow.credentials_repository.find_by_email(command.email)
            )
            if not creds:
                raise InvalidCredentialsException()

            profile = await uow.profile_repository.find_by_credentials_id(creds.oid)
            if not profile:
                raise InvalidCredentialsException()

        if not Password.check_passwords(password1=command.password, password2=creds.password):
            raise InvalidCredentialsException()

        profile_id_str = str(profile.oid)
        auth_data = self.jwt_service.generate_auth_tokens(profile_id=profile_id_str)

        self.redis_service.set(
            key=auth_data.refresh_token,
            value=profile_id_str,
            ttl=auth_data.refresh_expires,
        )

        return auth_data


@dataclass(frozen=True)
class ExtractProfileFromJWTTokenCommand(BaseCommand):
    token: str


@dataclass(frozen=True)
class ExtractProfileFromJWTTokenHandler(CommandHandler[ExtractProfileFromJWTTokenCommand, Profile]):
    user_uow: UserUoW
    jwt_service: BaseJWTService

    async def handle(self, command: ExtractProfileFromJWTTokenCommand) -> Profile:
        profile_id = self.jwt_service.decode_jwt_token(token=command.token)
        if not profile_id:
            raise UnauthorizedException()

        async with self.user_uow as uow:
            profile_model = await uow.profile_repository.find_by_id(profile_id)
            if not profile_model:
                raise UnauthorizedException()

        profile_entity = convert_profile_model_to_entity(profile_model)
        return profile_entity
