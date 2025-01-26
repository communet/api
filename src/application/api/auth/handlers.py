from fastapi import APIRouter, status, Depends, HTTPException
from punq import Container

from src.application.api.auth.schemas import RegisterResponseSchema, RegisterRequestSchema
from src.application.api.schemas import ErrorSchema
from src.domain.exceptions.base import ApplicationException
from src.logic.commands.auth import RegisterCommand
from src.logic.init.container import init_container
from src.logic.init.mediator import Mediator

router = APIRouter(tags=["Auth"])


@router.post(
    path='/auth/register',
    status_code=status.HTTP_201_CREATED,
    description="Create a new user",
    responses={
        status.HTTP_201_CREATED: {"model": RegisterResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema}
    },
)
async def register(
        schema: RegisterRequestSchema,
        container: Container = Depends(init_container),
) -> RegisterResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        profile, *_ = await mediator.handle_command(RegisterCommand(
            display_name=schema.display_name,
            username=schema.username,
            email=schema.email,
            password=schema.password,
            avatar=schema.avatar,
        ))
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message})
    return RegisterResponseSchema.from_entity(profile)
