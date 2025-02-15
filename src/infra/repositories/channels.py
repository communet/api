from abc import abstractmethod
from dataclasses import dataclass
from typing import Iterable, Sequence
from uuid import UUID, uuid4

from sqlalchemy import func, select, update
from sqlalchemy.orm import contains_eager

from src.domain.entities.channels import Channel
from src.domain.entities.users import Profile
from src.infra.filters.channels import GetAllChannelsInfraFilters
from src.infra.models.channels import ChannelMembersModel, ChannelModel
from src.infra.models.users import ProfileModel
from src.infra.repositories.base import BaseRepository


@dataclass(eq=False, frozen=True)
class BaseChannelRepository(BaseRepository):
    @abstractmethod
    async def get_all_channels(
        self,
        filters: GetAllChannelsInfraFilters,
        profile_id: UUID,
    ) -> tuple[Sequence[ChannelModel], int]:
        ...

    @abstractmethod
    async def get_channel_by_id(
        self,
        channel_id: UUID,
        profile_id: UUID,
        check_on_member: bool = True,
    ) -> ChannelModel | None:
        ...

    @abstractmethod
    async def update_channel(self, channel: Channel) -> None:
        ...

    @abstractmethod
    async def delete_channel_by_id(self, channel_id: UUID) -> None:
        ...

    @abstractmethod
    async def create(self, author: Profile, channel: Channel) -> ChannelModel:
        ...

    @abstractmethod
    async def get_members_by_channel_id(self, channel_id: UUID) -> Iterable[ProfileModel]:
        ...

    @abstractmethod
    async def connect_to_channel(self, channel_id: UUID, profile_id: UUID) -> bool:
        ...

    @abstractmethod
    async def disconnect_from_channel(self, channel_id: UUID, profile_id: UUID) -> bool:
        ...


@dataclass(eq=False, frozen=True)
class ChannelRepository(BaseChannelRepository):
    async def get_all_channels(
        self,
        filters: GetAllChannelsInfraFilters,
        profile_id: UUID,
    ) -> tuple[Sequence[ChannelModel], int]:
        async with self._session as session:
            channels_stmt = (
                select(ChannelModel)
                .join(ChannelMembersModel, ChannelModel.profiles)
                .where(
                    ChannelMembersModel.profile_id == profile_id,
                    ChannelMembersModel.is_connected == True,
                    ChannelModel.is_deleted == False,
                )
                .options(contains_eager(ChannelModel.profiles))
                .limit(filters.limit)
                .offset(filters.offset)
            )
            result = await session.execute(channels_stmt)
            channels = result.unique().scalars().all()

            channels_count_stmt = (
                select(func.count())
                .select_from(ChannelModel)
                .join(ChannelMembersModel, ChannelModel.profiles)
                .where(ChannelMembersModel.profile_id == profile_id)
            )
            channels_count = await session.scalar(channels_count_stmt)

            return channels, channels_count

    async def create(self, author: Profile, channel: Channel) -> ChannelModel:
        async with self._session as session:
            channel_model = ChannelModel(
                oid=channel.oid,
                name=channel.name.as_generic_type(),
                description=channel.description,
                avatar=channel.avatar,
            )
            channel_author = ChannelMembersModel(
                oid=uuid4(),
                profile_id=author.oid,
                channel_id=channel.oid,
            )

            session.add(channel_model)
            session.add(channel_author)

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

    async def get_channel_by_id(
        self,
        channel_id: UUID,
        profile_id: UUID,
        check_on_member: bool = True,
    ) -> ChannelModel | None:
        async with self._session as session:
            if check_on_member:
                stmt = (
                    select(ChannelModel)
                    .join(ChannelMembersModel, ChannelModel.profiles)
                    .where(
                        ChannelModel.oid == channel_id,
                        ChannelMembersModel.profile_id == profile_id,
                        ChannelModel.is_deleted == False,
                    )
                    .options(contains_eager(ChannelModel.profiles))
                )
            else:
                stmt = (
                    select(ChannelModel)
                    .join(ChannelMembersModel, ChannelModel.profiles)
                    .where(ChannelModel.oid == channel_id, ChannelModel.is_deleted == False)
                    .options(contains_eager(ChannelModel.profiles))
                )
            result = await session.execute(stmt)
            return result.unique().scalar_one_or_none()

    async def delete_channel_by_id(self, channel_id: UUID) -> None:
        async with self._session as session:
            stmt = update(ChannelModel).where(ChannelModel.oid == channel_id).values(is_deleted=True)
            await session.execute(stmt)
            await session.commit()

    async def connect_to_channel(self, channel_id: UUID, profile_id: UUID) -> bool:
        async with self._session as session:
            stmt = (
                select(ChannelMembersModel)
                .where(ChannelMembersModel.channel_id == channel_id, ChannelMembersModel.profile_id == profile_id)
            )

            result = True
            stmt_result = await session.execute(stmt)
            row: ChannelMembersModel = stmt_result.scalar_one_or_none()

            if row and row.is_connected:
                result = False
            elif row:
                row.is_connected = True
                session.add(row)
                await session.commit()
            else:
                new_row = ChannelMembersModel(oid=uuid4(), channel_id=channel_id, profile_id=profile_id)
                session.add(new_row)
                await session.commit()

            return result

    async def disconnect_from_channel(self, channel_id: UUID, profile_id: UUID) -> bool:
        async with self._session as session:
            stmt = (
                select(ChannelMembersModel)
                .where(ChannelMembersModel.channel_id == channel_id, ChannelMembersModel.profile_id == profile_id)
            )

            result = True
            stmt_result = await session.execute(stmt)
            row: ChannelMembersModel = stmt_result.scalar_one_or_none()

            if row and row.is_connected:
                row.is_connected = False
                session.add(row)
                await session.commit()
            else:
                result = False

            return result

    async def get_members_by_channel_id(self, channel_id: UUID) -> Iterable[ProfileModel]:
        async with self._session as session:
            query = (
                select(ProfileModel)
                .join(ChannelMembersModel, ProfileModel.oid == ChannelMembersModel.profile_id)
                .join(ChannelModel, ChannelMembersModel.channel_id == ChannelModel.oid)
                .where(
                    ChannelModel.oid == channel_id,
                    ChannelModel.is_deleted == False,
                    ChannelMembersModel.is_connected == True,
                )
                .options(
                    contains_eager(ProfileModel.channels),
                    contains_eager(ProfileModel.credentials),
                )
            )
            result = await session.execute(query)
            return result.unique().scalars().all()
