from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.models.base import Base


class CredentialsModel(Base):
    __tablename__ = "credentials"

    username: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
    profile: Mapped["ProfileModel"] = relationship(back_populates="credentials")


class ProfileModel(Base):
    __tablename__ = "profiles"

    display_name: Mapped[str] = mapped_column(String(255))
    avatar: Mapped[str] = mapped_column(String(255))
    credentials: Mapped["CredentialsModel"] = relationship(back_populates="profile")
