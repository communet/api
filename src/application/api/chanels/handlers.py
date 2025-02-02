from fastapi import APIRouter, Depends, HTTPException, status

from punq import Container

from src.application.api.auth.depends import get_current_user
from src.application.api.chanels.schemas import CreateChanelRequestSchema, CreateChanelResponseSchema
from src.application.api.schemas import ErrorSchema
from src.domain.entities.users import Profile
from src.domain.exceptions.base import ApplicationException
from src.logic.commands.chanels import CreateChanelCommand
from src.logic.init.container import init_container
from src.logic.init.mediator import Mediator


router = APIRouter(tags=["Chanels"])


@router.post(
    path='/chanels',
    status_code=status.HTTP_201_CREATED,
    description="Create a new chanel",
    responses={
        status.HTTP_201_CREATED: {"model": CreateChanelRequestSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema}
    },
)
async def create_chanel(
        schema: CreateChanelRequestSchema,
		_ = Depends(get_current_user),  # FIXME: Its need for protect route. Change to more useful depends without user
        container: Container = Depends(init_container),
) -> CreateChanelResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        chanel, *_ = await mediator.handle_command(CreateChanelCommand(
			name=schema.name,
            description=schema.description,
            avatar=schema.avatar,
        ))
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message})
    return CreateChanelResponseSchema.from_entity(chanel)
