from functools import lru_cache

from punq import Container, Scope

from src.infra.repositories.channels import BaseChannelRepository, ChannelRepository
from src.infra.repositories.users import UserUoW
from src.infra.services.jwt import BaseJWTService, JWTService
from src.infra.services.redis import BaseRedisService, RedisService
from src.logic.commands.auth import (
	ExtractProfileFromJWTTokenCommand,
	ExtractProfileFromJWTTokenHandler,
	LoginCommand,
	LoginCommandHandler,
	RefreshTokensCommand,
	RefreshTokensCommandHandler,
	RegisterCommandHandler,
	RegisterCommand,
)
from src.logic.commands.channels import (
    CreateChannelCommand,
    CreateChannelCommandHandler,
    DeleteChannelCommand,
    DeleteChannelCommandHandler,
)
from src.logic.init.mediator import Mediator
from src.settings.config import settings


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    def jwt_factory() -> BaseJWTService:
        return JWTService(settings())

    def redis_factory() -> BaseRedisService:
        return RedisService(settings())

    container.register(BaseChannelRepository, factory=ChannelRepository, scope=Scope.singleton)
    container.register(UserUoW, factory=UserUoW, scope=Scope.singleton)
    container.register(BaseRedisService, factory=redis_factory, scope=Scope.singleton)
    container.register(BaseJWTService, factory=jwt_factory, scope=Scope.singleton)

    def init_mediator() -> Mediator:
        mediator = Mediator()

		# Authenticate handlers
        register_new_user_handler = RegisterCommandHandler(
            user_uow=container.resolve(UserUoW),
        )
        user_login_handler = LoginCommandHandler(
            jwt_service=container.resolve(BaseJWTService),
            redis_service=container.resolve(BaseRedisService),
            user_uow=container.resolve(UserUoW),
        )
        extract_profile_handler = ExtractProfileFromJWTTokenHandler(
            jwt_service=container.resolve(BaseJWTService),
            user_uow=container.resolve(UserUoW),
        )
        refresh_tokens_handler = RefreshTokensCommandHandler(
            jwt_service=container.resolve(BaseJWTService),
            redis_service=container.resolve(BaseRedisService),
        )

        # Channel handlers
        create_channel_handler = CreateChannelCommandHandler(
            channel_repository=container.resolve(BaseChannelRepository),
        )
        delete_channel_handler = DeleteChannelCommandHandler(
            channel_repository=container.resolve(BaseChannelRepository),
        )

        mediator.register_command(
            command=RegisterCommand,
            command_handlers=[register_new_user_handler],
        )
        mediator.register_command(
            command=LoginCommand,
            command_handlers=[user_login_handler],
        )
        mediator.register_command(
            command=ExtractProfileFromJWTTokenCommand,
            command_handlers=[extract_profile_handler],
        )
        mediator.register_command(
            command=RefreshTokensCommand,
            command_handlers=[refresh_tokens_handler],
        )
        mediator.register_command(
            command=CreateChannelCommand,
            command_handlers=[create_channel_handler],
        )
        mediator.register_command(
            command=DeleteChannelCommand,
            command_handlers=[delete_channel_handler],
        )

        return mediator

    container.register(Mediator, factory=init_mediator)

    return container
