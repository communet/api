from functools import lru_cache

from punq import Container, Scope

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

    container.register(UserUoW, factory=UserUoW, scope=Scope.singleton)
    container.register(BaseRedisService, factory=redis_factory, scope=Scope.singleton)
    container.register(BaseJWTService, factory=jwt_factory, scope=Scope.singleton)

    def init_mediator() -> Mediator:
        mediator = Mediator()

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

        return mediator

    container.register(Mediator, factory=init_mediator)

    return container
