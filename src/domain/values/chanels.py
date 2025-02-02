from dataclasses import dataclass

from src.domain.exceptions.chanels import (
	ChanelNameEmptyException,
	ChanelNameTooLongException,
	ChanelNameTooShortException,
)
from src.domain.values.base import BaseValue


@dataclass(frozen=True)
class ChanelName(BaseValue[str]):
    def _validate(self) -> None:
        min_len = 3
        max_len = 32

        if not self.value:
            raise ChanelNameEmptyException()
        if len(self.value) < min_len:
            raise ChanelNameTooShortException(min_len)
        if len(self.value) > max_len:
            raise ChanelNameTooLongException(max_len)
