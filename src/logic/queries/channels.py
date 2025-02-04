from dataclasses import dataclass
from uuid import UUID

from src.domain.entities.channels import Channel
from src.infra.converters.chanels import convert_channel_model_to_entity
from src.infra.repositories.channels import BaseChannelRepository
from src.logic.exceptions.chanels import ChannelDoesNotExistsException
from src.logic.queries.base import BaseQuery, QueryHandler


@dataclass(frozen=True)
class GetChannelByOidQuery(BaseQuery):
    channel_oid: UUID


@dataclass(frozen=True)
class GetChannelByOidQueryHandler(QueryHandler[GetChannelByOidQuery, Channel]):
    channel_repository: BaseChannelRepository

    async def handle(self, query: GetChannelByOidQuery) -> Channel:
        channel_model = await self.channel_repository.get_channel_by_id(channel_id=query.channel_oid)

        if not channel_model:
            raise ChannelDoesNotExistsException(channel_id=query.channel_oid)

        channel = convert_channel_model_to_entity(channel_model=channel_model)
        return channel
