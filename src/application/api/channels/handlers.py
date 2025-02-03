from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from punq import Container

from src.application.api.auth.depends import get_current_user
from src.application.api.channels.schemas import CreateChannelRequestSchema, CreateChannelResponseSchema
from src.application.api.schemas import ErrorSchema
from src.domain.exceptions.base import ApplicationException
from src.logic.commands.channels import CreateChannelCommand, DeleteChannelCommand
from src.logic.init.container import init_container
from src.logic.init.mediator import Mediator


router = APIRouter(tags=["Channels"])


@router.post(
    path='/channels',
    status_code=status.HTTP_201_CREATED,
    description="Create a new channel",
    responses={
        status.HTTP_201_CREATED: {"model": CreateChannelRequestSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema}
    },
)
async def create_channel(
    schema: CreateChannelRequestSchema,
    _ = Depends(get_current_user),  # FIXME: Its need for protect route. Change to more useful depends without user
    container: Container = Depends(init_container),
) -> CreateChannelResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        channel, *_ = await mediator.handle_command(CreateChannelCommand(
			name=schema.name,
            description=schema.description,
            avatar=schema.avatar,
        ))
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message})
    return CreateChannelResponseSchema.from_entity(channel)


@router.delete(
    path='/channels/{channel_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete exists channel",
    responses={status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema}},
)
async def delete_channel(
    channel_id: UUID,
    _ = Depends(get_current_user),  # FIXME: Its need for protect route. Change to more useful depends without user
    container: Container = Depends(init_container),
) -> None:
    mediator: Mediator = container.resolve(Mediator)

    try:
        await mediator.handle_command(DeleteChannelCommand(channel_id=channel_id))
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message})
