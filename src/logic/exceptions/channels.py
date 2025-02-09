from dataclasses import dataclass
from uuid import UUID

from src.logic.exceptions.base import LogicException


@dataclass(eq=False)
class ChannelDoesNotExistsException(LogicException):
    channel_id: UUID

    @property
    def message(self) -> str:
        return f"Channel with given id({str(self.channel_id)}) does not exists"
