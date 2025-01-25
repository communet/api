from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.users import Credentials, Profile
from src.infra.database import DatabaseManager
from src.infra.models.users import CredentialsModel, ProfileModel
from src.infra.repositories.base import BaseRepository, BaseUoW


@dataclass(eq=False, frozen=True)
class CredentialsRepository(BaseRepository):
    async def create(self, credentials: Credentials) -> CredentialsModel:
        """
        Create a new user credentials. Add user credentials model to session by UserUoW.
        :param credentials: user credentials as Credentials entity.
        :return: model of user credentials.
        """
        credentials_model = CredentialsModel(
            oid=credentials.oid,
            username=credentials.username.as_generic_type(),
            email=credentials.email.as_generic_type(),
            password=credentials.password.as_generic_type(),
        )
        self._session.add(credentials_model)
        await self._session.flush()
        return credentials_model


@dataclass(eq=False, frozen=True)
class ProfileRepository(BaseRepository):
    async def create(self, profile: Profile) -> ProfileModel:
        """
        Create a new user profile. Add user profile model to session by UserUoW.
        :param profile: user profile as Profile entity.
        :return: model of user profile.
        """
        profile_model = ProfileModel(
            oid=profile.oid,
            display_name=profile.display_name.as_generic_type(),
            avatar=profile.avatar,
            credentials_id=profile.credentials.oid,
        )
        self._session.add(profile_model)
        await self._session.flush()
        return profile_model


class UserUoW(BaseUoW):
    def __init__(self, session: AsyncSession = DatabaseManager().get_test_session()):
        super().__init__(session)
        self.profile_repository = ProfileRepository(self._session)
        self.credentials_repository = CredentialsRepository(self._session)
