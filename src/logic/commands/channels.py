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
        chanel = Channel.create(
            name=command.name,
            description=command.description,
            avatar=command.avatar,
        )

        await self.channel_repository.create(channel=chanel)

        return chanel


@dataclass(frozen=True)
class DeleteChannelCommand:
    chanel_id: UUID


@dataclass(frozen=True)
class DeleteChannelCommandHandler(CommandHandler[DeleteChannelCommand, None]):
    channel_repository: BaseChannelRepository

    async def handle(self, command: DeleteChannelCommand) -> None:
        chanel_model = await self.channel_repository.get_channel_by_id(channel_id=command.chanel_id)

        if not chanel_model:
            raise ChannelDoesNotExistsException(channel_id=command.chanel_id)

        chanel = convert_channel_model_to_entity(chanel_model)
        chanel.delete()

        await self.channel_repository.delete_channel_by_id(channel_id=command.chanel_id)
