from dataclasses import dataclass
from uuid import UUID

from src.logic.exceptions.base import LogicException


@dataclass(eq=False)
class ChannelDoesNotExistsException(LogicException):
    channel_id: UUID

    @property
    def message(self) -> str:
        return f"Channel with given id({str(self.channel_id)}) does not exists"


@dataclass(eq=False)
class UserAlreadyMemberException(LogicException):
    channel_id: UUID
    profile_id: UUID

    @property
    def message(self) -> str:
        return f"The user ({str(self.profile_id)}) is already a member of a channel ({str(self.channel_id)})"


@dataclass(eq=False)
class UserAlreadyDisconnectedFromChannelException(LogicException):
    channel_id: UUID
    profile_id: UUID

    @property
    def message(self) -> str:
        return f"The user ({str(self.profile_id)}) is already disconnected from channel ({str(self.channel_id)})"
