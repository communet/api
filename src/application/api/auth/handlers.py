from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from punq import Container

from src.application.api.auth.schemas import (
	LoginRequestSchema,
	LoginResponseSchema,
	RefreshResponseSchema,
	RegisterResponseSchema,
	RegisterRequestSchema,
)
from src.application.api.schemas import ErrorSchema
from src.domain.exceptions.base import ApplicationException
from src.logic.commands.auth import LoginCommand, RefreshTokensCommand, RegisterCommand
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


@router.post(
    path='/auth/login',
    status_code=status.HTTP_200_OK,
    description="Login exists user",
    responses={
        status.HTTP_200_OK: {"model": LoginResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema}
    },
)
async def login(
    schema: LoginRequestSchema,
    response: Response,
    container: Container = Depends(init_container),
) -> LoginResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    try: 
        is_email = schema.is_email()

        auth_data, *_ = await mediator.handle_command(LoginCommand(
            username=schema.username if not is_email else None,
            email=schema.username if is_email else None,
            password=schema.password,
        ))

        response.set_cookie(
            key="refresh_token",
            value=auth_data.refresh_token,
            max_age=auth_data.refresh_expires.seconds,
            httponly=True,
        )
    except ApplicationException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "invalid credentials"})
    return LoginResponseSchema.from_entity(auth_data)


@router.post(
    path='/auth/refresh',
    status_code=status.HTTP_200_OK,
    description="Refresh tokens for user",
    responses={
        status.HTTP_200_OK: {"model": RefreshResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema}
    },
)
async def refresh(
    request: Request,
    response: Response,
    container: Container = Depends(init_container),
) -> RefreshResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        refresh = request.cookies.pop("refresh_token")
        if not refresh:
            raise ApplicationException()

        auth_data, *_ = await mediator.handle_command(RefreshTokensCommand(refresh_token=refresh))

        response.set_cookie(
            key="refresh_token",
            value=auth_data.refresh_token,
            max_age=auth_data.refresh_expires.seconds,
            httponly=True,
        )
    except ApplicationException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "refresh token was expired"})
    return RefreshResponseSchema.from_entity(auth_data)
