from abc import abstractmethod
from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from sqlalchemy import func, select, update

from src.domain.entities.channels import Channel
from src.infra.filters.channels import GetAllChannelsInfraFilters
from src.infra.models.channels import ChannelModel
from src.infra.repositories.base import BaseRepository


@dataclass(eq=False, frozen=True)
class BaseChannelRepository(BaseRepository):
    @abstractmethod
    async def get_all_channels(self, filters: GetAllChannelsInfraFilters) -> tuple[Sequence[ChannelModel], int]:
        ...

    @abstractmethod
    async def get_channel_by_id(self, channel_id: UUID) -> Channel:
        ...

    @abstractmethod
    async def update_channel(self, channel: Channel) -> None:
        ...

    @abstractmethod
    async def delete_channel_by_id(self, channel_id: UUID) -> bool:
        ...

    @abstractmethod
    async def create(self, channel: Channel) -> ChannelModel:
        ...


@dataclass(eq=False, frozen=True)
class ChannelRepository(BaseChannelRepository):
    async def get_all_channels(self, filters: GetAllChannelsInfraFilters) -> tuple[Sequence[ChannelModel], int]:
        async with self._session as session:
            stmt = select(ChannelModel).limit(filters.limit).offset(filters.offset)
            result = await session.execute(stmt)
            items = result.scalars().all()
            total_count = await session.scalar(select(func.count()).select_from(ChannelModel))

            return items, total_count

    async def create(self, channel: Channel) -> ChannelModel:
        async with self._session as session:
            channel_model = ChannelModel(
                oid=channel.oid,
                name=channel.name.as_generic_type(),
                description=channel.description,
                avatar=channel.avatar,
            )

            session.add(channel_model)
            await session.commit()

    async def update_channel(self, channel: Channel) -> None:
        async with self._session as session:
            stmt = (
                update(ChannelModel)
                .where(ChannelModel.oid == channel.oid)
                .values(
                    name=channel.name.as_generic_type(),
                    description=channel.description,
                    avatar=channel.avatar,
                )
            )
            await session.execute(stmt)
            await session.commit()

    async def get_channel_by_id(self, channel_id: UUID) -> ChannelModel | None:
        async with self._session as session:
            stmt = select(ChannelModel).where(ChannelModel.oid == channel_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def delete_channel_by_id(self, channel_id: UUID) -> None:
        async with self._session as session:
            stmt = update(ChannelModel).where(ChannelModel.oid == channel_id).values(is_deleted=True)
            await session.execute(stmt)
            await session.commit()
