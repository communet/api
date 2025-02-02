from dataclasses import dataclass

from src.domain.entities.chanels import Chanel
from src.infra.repositories.chanels import BaseChanelRepository
from src.logic.commands.base import CommandHandler


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
