from src.application.api.schemas import BaseRequestSchema, BaseResponseSchema
from src.domain.entities.chanels import Chanel


class CreateChanelRequestSchema(BaseRequestSchema):
	name: str
	description: str | None = None
	avatar: str | None = None


class CreateChanelResponseSchema(BaseResponseSchema):
	name: str
	description: str | None
	avatar: str | None

	@classmethod
	def from_entity(cls, entity: Chanel) -> "CreateChanelResponseSchema":
		return cls(
			name=entity.name.as_generic_type(),
			description=entity.description,
			avatar=entity.avatar,
		)
