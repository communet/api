from dataclasses import dataclass
from uuid import UUID

from src.logic.exceptions.base import LogicException


@dataclass(eq=False)
class ChanelDoesNotExistsException(LogicException):
    chanel_id: UUID

    @property
    def message(self) -> str:
        return f"Chanel with given id({str(self.chanel_id)}) does not exists"
