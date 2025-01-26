from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable, Type

from src.logic.commands.base import CT, CommandHandler, CR, BaseCommand
from src.logic.exceptions.mediator import CommandHandlersNotRegisteredException


@dataclass(eq=False)
class Mediator:
    # TODO: add events and queries here
    commands_map: dict[CT, list[CommandHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    def register_command(self, command: type(CT), command_handlers: Iterable[CommandHandler[CT, CR]]):
        """Register command handlers for command by command type"""
        self.commands_map[command].extend(command_handlers)

    async def handle_command(self, command: BaseCommand) -> Iterable[CR]:
        """
        Find command handler by command type and return handle result.
        :return: iterable results of registered command handlers
        """
        command_type: Type[CT] = command.__class__
        handlers = self.commands_map.get(command_type)

        if not handlers:
            raise CommandHandlersNotRegisteredException(command_type)

        return [await handler.handle(command) for handler in handlers]
