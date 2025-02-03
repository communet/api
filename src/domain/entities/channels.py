from dataclasses import dataclass, field

from src.domain.entities.base import BaseEntity
from src.domain.values.channels import ChannelName


@dataclass(eq=False)
class Channel(BaseEntity):
    name: ChannelName
    description: str | None
    avatar: str | None
    is_deleted: bool = field(
        default=False,
        kw_only=True,
    ) 

    @classmethod
    def create(cls, name: str, description: str | None, avatar: str | None, is_deleted: bool = False) -> "Channel":
        chanel = cls(
            name=ChannelName(name),
            description=description,
            is_deleted=is_deleted,
            avatar=avatar,
        )

        # NOTE: register events here

        return chanel

    def delete(self) -> None:
        # NOTE: method for register events on delete
        self.is_deleted = True
