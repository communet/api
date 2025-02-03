from dataclasses import dataclass
from uuid import UUID

from src.domain.entities.channels import Channel
from src.infra.converters.chanels import convert_channel_model_to_entity
from src.infra.repositories.channels import BaseChannelRepository
from src.logic.commands.base import CommandHandler
from src.logic.exceptions.chanels import ChannelDoesNotExistsException


@dataclass(frozen=True)
class CreateChannelCommand:
    name: str
    description: str | None
    avatar: str | None


@dataclass(frozen=True)
class CreateChannelCommandHandler(CommandHandler[CreateChannelCommand, Channel]):
    channel_repository: BaseChannelRepository

    async def handle(self, command: CreateChannelCommand) -> Channel:
        channel = Channel.create(
            name=command.name,
            description=command.description,
            avatar=command.avatar,
        )

        await self.channel_repository.create(channel=channel)

        return channel


@dataclass(frozen=True)
class UpdateChannelCommand:
    channel_id: UUID
    name: str | None
    description: str | None
    avatar: str | None


@dataclass(frozen=True)
class UpdateChannelCommandHandler(CommandHandler[UpdateChannelCommand, Channel]):
    channel_repository: BaseChannelRepository

    async def handle(self, command: UpdateChannelCommand) -> Channel:
        channel_model = await self.channel_repository.get_channel_by_id(channel_id=command.channel_id)

        if not channel_model:
            raise ChannelDoesNotExistsException(channel_id=command.channel_id)

        channel = convert_channel_model_to_entity(channel_model)
        channel.update(
            name=command.name,
            description=command.description,
            avatar=command.avatar,
        )

        await self.channel_repository.update_channel(channel=channel)
        return channel


@dataclass(frozen=True)
class DeleteChannelCommand:
    channel_id: UUID


@dataclass(frozen=True)
class DeleteChannelCommandHandler(CommandHandler[DeleteChannelCommand, None]):
    channel_repository: BaseChannelRepository

    async def handle(self, command: DeleteChannelCommand) -> None:
        channel_model = await self.channel_repository.get_channel_by_id(channel_id=command.channel_id)

        if not channel_model:
            raise ChannelDoesNotExistsException(channel_id=command.channel_id)

        channel = convert_channel_model_to_entity(channel_model)
        channel.delete()

        await self.channel_repository.delete_channel_by_id(channel_id=command.channel_id)
