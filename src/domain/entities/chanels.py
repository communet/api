from dataclasses import dataclass, field

from src.domain.entities.base import BaseEntity
from src.domain.values.chanels import ChanelName


@dataclass(eq=False)
class Chanel(BaseEntity):
    name: ChanelName
    description: str | None
    avatar: str | None
    is_deleted: bool = field(
        default=False,
        kw_only=True,
    ) 

    @classmethod
    def create(cls, name: str, description: str | None, avatar: str | None, is_deleted: bool = False) -> "Chanel":
        chanel = cls(
            name=ChanelName(name),
            description=description,
            is_deleted=is_deleted,
            avatar=avatar,
        )

        # NOTE: register events here

        return chanel

    def delete(self) -> None:
        # NOTE: method for register events on delete
        self.is_deleted = True
