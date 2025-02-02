from dataclasses import dataclass

from src.domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class ChanelNameEmptyException(ApplicationException):
    @property
    def message(self) -> str:
        return "Chanel name can't be empty"


@dataclass(eq=False)
class ChanelNameTooShortException(ApplicationException):
    min_len: int

    @property
    def message(self) -> str:
        return "Chanel name should be greater than or equal to {min_len}"


@dataclass(eq=False)
class ChanelNameTooLongException(ApplicationException):
    max_len: int

    @property
    def message(self) -> str:
        return "Chanel name should be less than or equal to {max_len}"
