from typing import Iterable
from src.application.api.schemas import BaseRequestSchema, BaseResponseSchema
from src.domain.entities.channels import Channel
from src.domain.entities.users import Profile
from src.infra.filters.channels import GetAllChannelsInfraFilters


class GetAllChannelsFilters(BaseRequestSchema):
    limit: int = 10
    offset: int = 0

    def to_infra(self) -> GetAllChannelsInfraFilters:
        return GetAllChannelsInfraFilters(limit=self.limit, offset=self.offset)


class GetAllChannelsResponseSchema(BaseResponseSchema):
    count: int
    offset: int
    limit: int
    # FIXME: replace dict to Channel + fix profblem with name field
    items: list[dict]

    @classmethod
    def from_entity(
        cls, count: int, limit: int, offset: int, entities: Iterable[Channel],
    ) -> "GetAllChannelsResponseSchema":
        return cls(
            count=count,
            offset=offset,
            limit=limit,
            items=[
                {
                    "oid": entity.oid,
                    "name": entity.name.as_generic_type(),
                    "description": entity.description,
                    "is_deleted": entity.is_deleted,
                    "avatar": entity.avatar,
                } for entity in entities
            ],
        )


class GetChannelByOidResponseSchema(BaseResponseSchema):
    oid: str
    name: str
    description: str | None
    avatar: str | None

    @classmethod
    def from_entity(cls, entity: Channel) -> "GetChannelByOidResponseSchema":
        return cls(
            oid=str(entity.oid),
            name=entity.name.as_generic_type(),
            description=entity.description,
            avatar=entity.avatar,
		)


class CreateChannelRequestSchema(BaseRequestSchema):
	name: str
	description: str | None = None
	avatar: str | None = None


class CreateChannelResponseSchema(BaseResponseSchema):
    oid: str
    name: str
    description: str | None
    members: Iterable
    avatar: str | None

    @classmethod
    def from_entity(cls, entity: Channel) -> "CreateChannelResponseSchema":
        return cls(
            oid=str(entity.oid),
            name=entity.name.as_generic_type(),
            description=entity.description,
            members=[
                {
                    "id": member.oid,
                    "display_name": member.display_name.as_generic_type(),
                    "username": member.credentials.username.as_generic_type(),
                    "email": member.credentials.email.as_generic_type(),
                    "avatar": member.avatar,
                }
                for member in entity.members
            ],
            avatar=entity.avatar,
		)


class UpdateChannelRequestSchema(BaseRequestSchema):
    name: str | None
    description: str | None
    avatar: str | None


class UpdateChannelResponseSchema(BaseResponseSchema):
    oid: str
    name: str
    description: str | None
    avatar: str | None

    @classmethod
    def from_entity(cls, entity: Channel) -> "CreateChannelResponseSchema":
        return cls(
            oid=str(entity.oid),
            name=entity.name.as_generic_type(),
            description=entity.description,
            avatar=entity.avatar,
        )
