from dataclasses import dataclass

from src.domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class UsernameEmptyException(ApplicationException):
    @property
    def message(self) -> str:
        return "Username can't be empty"


@dataclass(eq=False)
class UsernameTooShortException(ApplicationException):
    min_len: int

    @property
    def message(self) -> str:
        return "Username should be greater than or equal to {min_len}"


@dataclass(eq=False)
class UsernameTooLongException(ApplicationException):
    max_len: int

    @property
    def message(self) -> str:
        return "Username should be less than or equal to {max_len}"


@dataclass(eq=False)
class EmailInvalidFormatException(ApplicationException):
    @property
    def message(self) -> str:
        return "Invalid email format"


@dataclass(eq=False)
class EmailEmptyException(ApplicationException):
    @property
    def message(self) -> str:
        return "Email can't be empty"


@dataclass(eq=False)
class PasswordTooShortException(ApplicationException):
    min_len: 8

    @property
    def message(self) -> str:
        return "Password should be greater than or equal to {min_len}"


@dataclass(eq=False)
class PasswordEmptyException(ApplicationException):
    @property
    def message(self) -> str:
        return "Password can't be empty"
