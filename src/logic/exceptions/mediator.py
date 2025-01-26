from dataclasses import dataclass

from src.logic.exceptions.base import LogicException


@dataclass(eq=False)
class CommandHandlersNotRegisteredException(LogicException):
    command_type: type

    @property
    def message(self) -> str:
        return f"CommandHandler has not been registered for: {self.command_type}"
