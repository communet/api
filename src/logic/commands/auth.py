from dataclasses import dataclass

from src.domain.entities.users import Profile, Credentials
from src.infra.repositories.base import BaseUoW
from src.infra.repositories.users import UserUoW
from src.logic.commands.base import BaseCommand, CommandHandler
from src.logic.exceptions.users import UserAlreadyExistsException


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
