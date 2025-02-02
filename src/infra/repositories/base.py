from abc import ABC
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.database import DatabaseManager


@dataclass(eq=False, frozen=True)
class BaseRepository(ABC):
    """
    Base repository with common attributes and methods.
    :param _session: SQLAlchemy session for database operations.
    """
    _session: AsyncSession = DatabaseManager().get_test_session()


class BaseUoW(ABC):
    """
    Manages transactions and provides access to repositories.
    :param session: SQLAlchemy session for database operations.
    """
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def commit(self) -> None:
        """Commit the current transaction in progress."""
        await self._session.commit()

    async def rollback(self) -> None:
        """Rollback the current transaction in progress."""
        await self._session.rollback()

    async def __aenter__(self) -> "BaseUoW":
        """
        Enters the context manager.
        :return: The UnitOfWork instance.
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Exits the context manager.
        :param exc_type: The type of exception (if any).
        :param exc_val: The exception value (if any).
        :param exc_tb: The exception traceback (if any).
        """
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()
