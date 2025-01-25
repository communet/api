from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from typing import AsyncGenerator

from src.settings.config import settings


class DatabaseManager:
    def __init__(self):
        self.engine = create_async_engine(url=settings().get_db_url())
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session
            await session.close()

    def get_test_session(self) -> AsyncSession:
        return self.session_factory()
