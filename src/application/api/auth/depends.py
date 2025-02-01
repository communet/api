from profile import Profile
from typing import Container
from fastapi import Depends, status, HTTPException, Request

from src.domain.exceptions.base import ApplicationException
from src.logic.commands.auth import ExtractProfileFromJWTTokenCommand
from src.logic.init.container import init_container
from src.logic.init.mediator import Mediator


async def get_auth_token(request: Request) -> str:
	token = request.headers.get("Authorization")
	if not token:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"message": "auth token not found"})
	return token


async def get_current_user(
	token: str = Depends(get_auth_token),
	container: Container = Depends(init_container),
) -> Profile:
    mediator: Mediator = container.resolve(Mediator)

    try:
        profile, *_ = await mediator.handle_command(ExtractProfileFromJWTTokenCommand(token=token))
    except ApplicationException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "invalid credentials"})
    return profile
