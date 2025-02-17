from dataclasses import dataclass
from typing import Iterable
from uuid import UUID

from src.domain.entities.channels import Channel
from src.domain.entities.users import Profile
from src.infra.converters.channels import convert_channel_model_to_entity
from src.infra.converters.users import convert_profile_model_to_entity
from src.infra.filters.channels import GetAllChannelsInfraFilters
from src.infra.repositories.channels import BaseChannelRepository
from src.logic.exceptions.channels import ChannelDoesNotExistsException
from src.logic.queries.base import BaseQuery, QueryHandler


@dataclass(frozen=True)
class GetAllChannelsQuery(BaseQuery):
    filters: GetAllChannelsInfraFilters
    profile_id: UUID


@dataclass(frozen=True)
class GetAllChannelsQueryHandler(QueryHandler[GetAllChannelsQuery, tuple[Iterable[Channel], int]]):
    channel_repository: BaseChannelRepository

    async def handle(self, query: GetAllChannelsQuery) -> tuple[Iterable[Channel], int]:
        channel_models, channels_count = await self.channel_repository.get_all_channels(
            filters=query.filters,
            profile_id=query.profile_id,
        )
        channels = list(map(lambda model: convert_channel_model_to_entity(model), channel_models))
        return channels, channels_count


@dataclass(frozen=True)
class GetChannelByOidQuery(BaseQuery):
    channel_id: UUID
    profile_id: UUID


@dataclass(frozen=True)
class GetChannelByOidQueryHandler(QueryHandler[GetChannelByOidQuery, Channel]):
    channel_repository: BaseChannelRepository

    async def handle(self, query: GetChannelByOidQuery) -> Channel:
        channel_model = await self.channel_repository.get_channel_by_id(
            channel_id=query.channel_id,
            profile_id=query.profile_id,
            check_on_member=True,
        )

        if not channel_model:
            raise ChannelDoesNotExistsException(channel_id=query.channel_id)

        return convert_channel_model_to_entity(channel_model=channel_model)


@dataclass(frozen=True)
class GetAllChannelMembersQuery(BaseQuery):
    channel_id: UUID


@dataclass(frozen=True)
class GetAllChannelMembersQueryHandler(QueryHandler[GetAllChannelMembersQuery, Iterable[Profile]]):
    channel_repository: BaseChannelRepository

    async def handle(self, query: GetAllChannelMembersQuery) -> Iterable[Profile]:
        member_models = await self.channel_repository.get_members_by_channel_id(channel_id=query.channel_id)
        profiles = list(map(lambda model: convert_profile_model_to_entity(model), member_models))
        return profiles
