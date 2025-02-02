from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.infra.models.base import Base


class ChanelModel(Base):
    __tablename__ = "chanels"

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text(), nullable=True, default=None)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True, default=None)
