from typing import Iterable
from src.application.api.schemas import BaseRequestSchema, BaseResponseSchema
from src.domain.entities.channels import Channel
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
    avatar: str | None

    @classmethod
    def from_entity(cls, entity: Channel) -> "CreateChannelResponseSchema":
        return cls(
            oid=str(entity.oid),
            name=entity.name.as_generic_type(),
            description=entity.description,
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
