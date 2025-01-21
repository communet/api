from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.settings.config import settings


class DatabaseManager:
    def __init__(self):
        self.engine = create_async_engine(url=settings().get_db_url())
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def get_session(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session
            await session.close()
