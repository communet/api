from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import UUID

from src.domain.entities.base import BaseEntity
from src.domain.values.users import Email, Password, Username


@dataclass(eq=False)
class Credentials(BaseEntity):
    username: Username
    email: Email
    password: Password

    @classmethod
    def create(cls, username: str, email: str, password: str,) -> "Credentials":
        """
        Method for create credentials entity and register events.
        :return: instance of this class
        """
        return cls(
            username=Username(username),
            email=Email(email),
            password=Password(password),
        )


@dataclass(eq=False)
class Profile(BaseEntity):
    display_name: Username
    avatar: str
    credentials: Credentials

    @classmethod
    def create(cls, display_name: str, avatar: str, credentials: Credentials) -> "Profile":
        """
        Method for create profile entity and register events.
        :return: instance of this class
        """
        profile = cls(
            display_name=Username(display_name),
            avatar=avatar,
            credentials=credentials,
        )

        # TODO: register `NewUserRegisterEvent` here

        return profile


@dataclass(eq=False)
class AuthData(BaseEntity):
    access_token: str
    refresh_token: str
    access_expires: datetime
    refresh_expires: timedelta
