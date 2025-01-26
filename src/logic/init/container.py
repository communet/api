from functools import lru_cache

from punq import Container, Scope

from src.infra.repositories.users import UserUoW
from src.logic.commands.auth import RegisterCommandHandler, RegisterCommand
from src.logic.init.mediator import Mediator


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    # TODO: put other repositories here
    container.register(UserUoW, factory=UserUoW, scope=Scope.singleton)

    # TODO: put events and queries here

    # Command handlers
    container.register(RegisterCommandHandler)

    # Mediator
    def init_mediator() -> Mediator:
        mediator = Mediator()

        # Command handlers
        register_new_user_handler = RegisterCommandHandler(
            user_uow=container.resolve(UserUoW),
        )

        # TODO: register events and queries here
        # Commands
        mediator.register_command(
            command=RegisterCommand,
            command_handlers=[register_new_user_handler],
        )

        return mediator

    container.register(Mediator, factory=init_mediator)

    return container
