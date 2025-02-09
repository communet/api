from dataclasses import dataclass
from typing import Iterable
from uuid import UUID

from src.domain.entities.channels import Channel
from src.infra.converters.channels import convert_channel_model_to_entity
from src.infra.filters.channels import GetAllChannelsInfraFilters
from src.infra.repositories.channels import BaseChannelRepository
from src.logic.exceptions.channels import ChannelDoesNotExistsException
from src.logic.queries.base import BaseQuery, QueryHandler


@dataclass(frozen=True)
class GetAllChannelsQuery(BaseQuery):
    filters: GetAllChannelsInfraFilters


@dataclass(frozen=True)
class GetAllChannelsQueryHandler(QueryHandler[GetAllChannelsQuery, tuple[Iterable[Channel], int]]):
    channel_repository: BaseChannelRepository

    async def handle(self, query: GetAllChannelsQuery) -> tuple[Iterable[Channel], int]:
        channel_models, total_count = await self.channel_repository.get_all_channels(filters=query.filters)
        channels = list(map(lambda model: convert_channel_model_to_entity(model), channel_models))
        return channels, total_count


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
