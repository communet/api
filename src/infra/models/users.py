from uuid import UUID

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from src.infra.models.base import Base


class CredentialsModel(Base):
    __tablename__ = "credentials"

    username: Mapped[str] = mapped_column(String(255), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    profile: Mapped["ProfileModel"] = relationship(
        back_populates="credentials"
    )


class ProfileModel(Base):
    __tablename__ = "profiles"

    display_name: Mapped[str] = mapped_column(String(255))
    avatar: Mapped[str] = mapped_column(String(255))
    credentials_id: Mapped[UUID] = mapped_column(
        ForeignKey("credentials.oid", ondelete="CASCADE"),
        unique=True,
        type_=PGUUID(as_uuid=True),
    )
    credentials: Mapped["CredentialsModel"] = relationship(back_populates="profile")
