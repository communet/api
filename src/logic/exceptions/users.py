from dataclasses import dataclass

from src.logic.exceptions.base import LogicException


@dataclass(eq=False)
class UserAlreadyExistsException(LogicException):
    email: str
    username: str

    @property
    def message(self) -> str:
        return f"User with given email({self.email}) and username({self.username}) already exists"
