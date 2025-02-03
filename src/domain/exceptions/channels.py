from dataclasses import dataclass

from src.domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class ChannelNameEmptyException(ApplicationException):
    @property
    def message(self) -> str:
        return "Channel name can't be empty"


@dataclass(eq=False)
class ChannelNameTooShortException(ApplicationException):
    min_len: int

    @property
    def message(self) -> str:
        return "Channel name should be greater than or equal to {min_len}"


@dataclass(eq=False)
class ChannelNameTooLongException(ApplicationException):
    max_len: int

    @property
    def message(self) -> str:
        return "Channel name should be less than or equal to {max_len}"
