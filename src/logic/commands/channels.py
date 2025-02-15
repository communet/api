from dataclasses import dataclass
from uuid import UUID

from src.domain.entities.channels import Channel
from src.domain.entities.users import Profile
from src.infra.converters.channels import convert_channel_model_to_entity
from src.infra.repositories.channels import BaseChannelRepository
from src.logic.commands.base import BaseCommand, CommandHandler
from src.logic.exceptions.channels import ChannelDoesNotExistsException, UserAlreadyDisconnectedFromChannelException, UserAlreadyMemberException


@dataclass(frozen=True)
class CreateChannelCommand(BaseCommand):
    name: str
    description: str | None
    author: Profile
    avatar: str | None


@dataclass(frozen=True)
class CreateChannelCommandHandler(CommandHandler[CreateChannelCommand, Channel]):
    channel_repository: BaseChannelRepository

    async def handle(self, command: CreateChannelCommand) -> Channel:
        channel = Channel.create(
            name=command.name,
            description=command.description,
            avatar=command.avatar,
            members=[command.author]
        )

        await self.channel_repository.create(author=command.author, channel=channel)
        return channel


@dataclass(frozen=True)
class UpdateChannelCommand(BaseCommand):
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
class DeleteChannelCommand(BaseCommand):
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


@dataclass(frozen=True)
class ConnectToChannelCommand(BaseCommand):
    channel_id: UUID
    profile_id: UUID


@dataclass(frozen=True)
class ConnectToChannelCommandHandler(CommandHandler[ConnectToChannelCommand, Channel]):
    channel_repository: BaseChannelRepository

    async def handle(self, command: ConnectToChannelCommand) -> Channel:
        channel_model = await self.channel_repository.get_channel_by_id(
            profile_id=command.profile_id,
            channel_id=command.channel_id,
            check_on_member=False,
        )
        if not channel_model:
            raise ChannelDoesNotExistsException(channel_id=command.channel_id)

        joined = await self.channel_repository.connect_to_channel(
            channel_id=command.channel_id,
            profile_id=command.profile_id,
        )
        if not joined:
            raise UserAlreadyMemberException(channel_id=command.channel_id, profile_id=command.profile_id)

        return convert_channel_model_to_entity(channel_model)


@dataclass(frozen=True)
class DisconnectFromChannelCommand(BaseCommand):
    channel_id: UUID
    profile_id: UUID


@dataclass(frozen=True)
class DisconnectFromChannelCommandHandler(CommandHandler[DisconnectFromChannelCommand, None]):
    channel_repository: BaseChannelRepository

    async def handle(self, command: DisconnectFromChannelCommand) -> None:
        channel_model = await self.channel_repository.get_channel_by_id(
            profile_id=command.profile_id,
            channel_id=command.channel_id,
        )
        if not channel_model:
            raise ChannelDoesNotExistsException(channel_id=command.channel_id)

        disconnected = await self.channel_repository.disconnect_from_channel(
            channel_id=command.channel_id,
            profile_id=command.profile_id,
        )
        if not disconnected:
            raise UserAlreadyDisconnectedFromChannelException(
                channel_id=command.channel_id,
                profile_id=command.profile_id,
            )
