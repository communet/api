from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.infra.models.base import Base


class ChanelModel(Base):
    __tablename__ = "chanels"

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text())
    avatar: Mapped[str] = mapped_column(String(255))
