from dataclasses import dataclass

from src.domain.exceptions.channels import (
	ChannelNameEmptyException,
	ChannelNameTooLongException,
	ChannelNameTooShortException,
)
from src.domain.values.base import BaseValue


@dataclass(frozen=True)
class ChannelName(BaseValue[str]):
    def _validate(self) -> None:
        min_len = 3
        max_len = 32

        if not self.value:
            raise ChannelNameEmptyException()
        if len(self.value) < min_len:
            raise ChannelNameTooShortException(min_len)
        if len(self.value) > max_len:
            raise ChannelNameTooLongException(max_len)
