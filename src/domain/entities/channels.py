from dataclasses import dataclass, field
from profile import Profile
from typing import Iterable

from src.domain.entities.base import BaseEntity
from src.domain.values.channels import ChannelName


@dataclass(eq=False)
class Channel(BaseEntity):
    name: ChannelName
    description: str | None
    avatar: str | None
    members: Iterable[Profile] = field(
        default_factory=list,
    )
    is_deleted: bool = field(
        default=False,
        kw_only=True,
    ) 

    @classmethod
    def create(
        cls,
        name: str,
        description: str | None,
        members: Iterable[Profile],
        avatar: str | None,
        is_deleted: bool = False,
    ) -> "Channel":
        chanel = cls(
            name=ChannelName(name),
            description=description,
            members=members,
            is_deleted=is_deleted,
            avatar=avatar,
        )

        # NOTE: register events here

        return chanel

    def update(self, name: str | None, description: str | None, avatar: str | None) -> None:
        self.name = ChannelName(name) if name else None
        self.description = description if description else None
        self.avatar = avatar if avatar else None

    def delete(self) -> None:
        # NOTE: method for register events on delete
        self.is_deleted = True
