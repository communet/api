from src.application.api.schemas import BaseRequestSchema, BaseResponseSchema
from src.domain.entities.users import Profile


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
