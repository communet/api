from dataclasses import dataclass
from uuid import UUID

from src.domain.entities.chanels import Chanel
from src.infra.converters.chanels import convert_chanel_model_to_entity
from src.infra.repositories.chanels import BaseChanelRepository
from src.logic.commands.base import CommandHandler
from src.logic.exceptions.chanels import ChanelDoesNotExistsException


@dataclass(frozen=True)
class CreateChanelCommand:
    name: str
    description: str | None
    avatar: str | None


@dataclass(frozen=True)
class CreateChanelCommandHandler(CommandHandler[CreateChanelCommand, Chanel]):
    chanel_repository: BaseChanelRepository

    async def handle(self, command: CreateChanelCommand) -> Chanel:
        chanel = Chanel.create(
            name=command.name,
            description=command.description,
            avatar=command.avatar,
        )

        await self.chanel_repository.create(chanel=chanel)

        return chanel


@dataclass(frozen=True)
class DeleteChanelCommand:
    chanel_id: UUID


@dataclass(frozen=True)
class DeleteChanelCommandHandler(CommandHandler[DeleteChanelCommand, None]):
    chanel_repository: BaseChanelRepository

    async def handle(self, command: DeleteChanelCommand) -> None:
        chanel_model = await self.chanel_repository.get_chanel_by_id(chanel_id=command.chanel_id)

        if not chanel_model:
            raise ChanelDoesNotExistsException(chanel_id=command.chanel_id)

        chanel = convert_chanel_model_to_entity(chanel_model)
        chanel.delete()

        await self.chanel_repository.delete_chanel_by_id(chanel_id=command.chanel_id)
