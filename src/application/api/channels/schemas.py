from uuid import UUID
from src.application.api.schemas import BaseRequestSchema, BaseResponseSchema
from src.domain.entities.channels import Channel


class CreateChannelRequestSchema(BaseRequestSchema):
	name: str
	description: str | None = None
	avatar: str | None = None


class CreateChannelResponseSchema(BaseResponseSchema):
	name: str
	description: str | None
	avatar: str | None

	@classmethod
	def from_entity(cls, entity: Channel) -> "CreateChannelResponseSchema":
		return cls(
			name=entity.name.as_generic_type(),
			description=entity.description,
			avatar=entity.avatar,
		)


class UpdateChannelRequestSchema(BaseRequestSchema):
    name: str | None
    description: str | None
    avatar: str | None


class UpdateChannelResponseSchema(BaseResponseSchema):
	name: str
	description: str | None
	avatar: str | None

	@classmethod
	def from_entity(cls, entity: Channel) -> "CreateChannelResponseSchema":
		return cls(
			name=entity.name.as_generic_type(),
			description=entity.description,
			avatar=entity.avatar,
		)
