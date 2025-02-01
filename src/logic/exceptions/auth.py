from dataclasses import dataclass

from src.logic.exceptions.base import LogicException


@dataclass(eq=False)
class UserAlreadyExistsException(LogicException):
    email: str
    username: str

    @property
    def message(self) -> str:
        return f"User with given email({self.email}) or username({self.username}) already exists"


@dataclass(eq=False)
class InvalidCredentialsException(LogicException):
    @property
    def message(self) -> str:
        return "Invalid credentials exception"


@dataclass(eq=False)
class UnauthorizedException(LogicException):
    @property
    def message(self) -> str:
        return "User is not authorized"
