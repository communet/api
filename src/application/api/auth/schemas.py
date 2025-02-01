import re

from datetime import datetime

from src.application.api.schemas import BaseRequestSchema, BaseResponseSchema
from src.domain.entities.users import AuthData, Profile


class RegisterRequestSchema(BaseRequestSchema):
    display_name: str
    username: str
    email: str
    password: str
    avatar: str


class RegisterResponseSchema(BaseResponseSchema):
    oid: str
    display_name: str
    username: str
    email: str
    avatar: str

    @classmethod
    def from_entity(cls, entity: Profile) -> "RegisterResponseSchema":
        return cls(
            oid=str(entity.oid),
            display_name=entity.display_name.as_generic_type(),
            username=entity.credentials.username.as_generic_type(),
            email=entity.credentials.email.as_generic_type(),
            avatar=entity.avatar,
        )


class LoginRequestSchema(BaseRequestSchema):
    username: str
    password: str

    def is_email(self) -> bool:
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
        return bool(re.fullmatch(pattern, self.username))


class LoginResponseSchema(BaseResponseSchema):
    access_token: str
    access_expires: datetime

    @classmethod
    def from_entity(cls, entity: AuthData) -> "LoginResponseSchema":
        return cls(
            access_token=entity.access_token,
            access_expires=entity.access_expires,
        )


class RefreshResponseSchema(BaseResponseSchema):
    access_token: str
    access_expires: datetime

    @classmethod
    def from_entity(cls, entity: AuthData) -> "RefreshResponseSchema":
        return cls(
            access_token=entity.access_token,
            access_expires=entity.access_expires,
        )