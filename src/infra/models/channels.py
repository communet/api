from uuid import UUID

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.models.base import Base


class ChannelModel(Base):
    __tablename__ = "channels"

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text(), nullable=True, default=None)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True, default=None)

    profiles: Mapped[list["ChannelMembersModel"]] = relationship(back_populates="channel")


class ChannelMembersModel(Base):
    __tablename__ = "channel_members"

    profile_id: Mapped[UUID] = mapped_column(ForeignKey("profiles.oid", ondelete="CASCADE"), type_=PGUUID(as_uuid=True))
    channel_id: Mapped[UUID] = mapped_column(ForeignKey("channels.oid", ondelete="CASCADE"), type_=PGUUID(as_uuid=True))
    # TODO: add field for roles here

    profile: Mapped["ProfileModel"] = relationship(back_populates="channels")
    channel: Mapped["ChannelModel"] = relationship(back_populates="profiles")
