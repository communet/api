import pytest

from src.domain.entities.users import Credentials, Profile
from src.domain.exceptions.users import UsernameEmptyException
from src.infra.database import DatabaseManager
from src.infra.repositories.users import UserUoW


pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_user_uow() -> None:
    credentials = Credentials.create("test_username", "test_main@mail.ru", "valid_password")
    profile = Profile.create("display_name", "avatar_url", credentials)

    async with UserUoW() as uow:
        await uow.credentials_repository.create(credentials)
        await uow.profile_repository.create(profile)
        await uow.commit()

    session = DatabaseManager().get_test_session()
    credentials = Credentials.create("new_test_username", "new_test_main@mail.ru", "new_valid_password")
    profile = Profile.create("new_display_name", "avatar_url", credentials)

    async with UserUoW(session) as uow:
        await uow.credentials_repository.create(credentials)
        await uow.profile_repository.create(profile)
        await uow.commit()

    session = DatabaseManager().get_test_session()
    with pytest.raises(UsernameEmptyException):
        async with UserUoW(session) as uow:
            credentials = Credentials.create(
                "new_again_test_username",
                "new_again_test_main@mail.ru",
                "new_again_valid_password",
            )
            await uow.credentials_repository.create(credentials)
            profile = Profile.create("", "avatar_url", credentials)
            await uow.profile_repository.create(profile)
            await uow.commit()
