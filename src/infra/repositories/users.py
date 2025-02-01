from abc import abstractmethod
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.domain.entities.users import Credentials, Profile
from src.infra.database import DatabaseManager
from src.infra.models.users import CredentialsModel, ProfileModel
from src.infra.repositories.base import BaseRepository, BaseUoW


@dataclass(eq=False, frozen=True)
class BaseCredentialsRepository(BaseRepository):
    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[CredentialsModel]:
        ...

    @abstractmethod
    async def find_by_username(self, username: str) -> Optional[CredentialsModel]:
        ...

    @abstractmethod
    async def create(self, credentials: Credentials) -> Optional[CredentialsModel]:
        ...

    @abstractmethod
    async def check_user_exists(self, email: str, username: str) -> bool:
        ...


@dataclass(eq=False, frozen=True)
class CredentialsRepository(BaseCredentialsRepository):
    async def find_by_email(self, email: str) -> Optional[CredentialsModel]:
        stmt = select(CredentialsModel).where(CredentialsModel.email == email)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_by_username(self, username: str) -> Optional[CredentialsModel]:
        stmt = select(CredentialsModel).where(CredentialsModel.username == username)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, credentials: Credentials) -> Optional[CredentialsModel]:
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

    async def check_user_exists(self, email: str, username: str) -> bool:
        """
        Check user exists with given email or username.
        :return: True if user exists else False.
        """
        stmt = select(CredentialsModel).where(
            or_(CredentialsModel.email == email, CredentialsModel.username == username)
        )
        result = await self._session.execute(stmt)
        return result.scalar() is not None


@dataclass(eq=False, frozen=True)
class BaseProfileRepository(BaseRepository):
    @abstractmethod
    async def find_by_id(self, profile_id: UUID) -> Optional[ProfileModel]:
        ...

    @abstractmethod
    async def find_by_credentials_id(self, credentials_id: UUID) -> Optional[ProfileModel]:
        ...

    @abstractmethod
    async def create(self, profile: Profile) -> Optional[ProfileModel]:
        ...


@dataclass(eq=False, frozen=True)
class ProfileRepository(BaseProfileRepository):
    async def find_by_id(self, profile_id) -> Optional[ProfileModel]:
        stmt = select(ProfileModel).where(ProfileModel.oid == profile_id).options(joinedload(ProfileModel.credentials))
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_by_credentials_id(self, credentials_id: UUID) -> Optional[ProfileModel]:
        stmt = select(ProfileModel).where(ProfileModel.credentials_id == credentials_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, profile: Profile) -> Optional[ProfileModel]:
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
        self.profile_repository: BaseProfileRepository = ProfileRepository(self._session)
        self.credentials_repository: BaseCredentialsRepository = CredentialsRepository(self._session)
