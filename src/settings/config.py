from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	API_PORT: int = Field(default=8000, alias="API_PORT")
	DEBUG: bool = Field(default=False, alias="API_DEBUG")
	POSTGRES_USER: str = Field(default="postgres", alias="POSTGRES_USER")
	POSTGRES_PASSWORD: str = Field(default="postgres", alias="POSTGRES_PASSWORD")
	POSTGRES_HOST: str = Field(default="postgres", alias="POSTGRES_HOST")
	POSTGRES_PORT: int = Field(default=5432, alias="POSTGRES_PORT")
	POSTGRES_DB: str = Field(default="communet_db", alias="POSTGRES_DB")
	REDIS_HOST: str = Field(default="redis", alias="REDIS_HOST")
	REDIS_PORT: int = Field(default=6379, alias="REDIS_PORT")
	REDIS_DB: int = Field(default=0, alias="REDIS_DB")

	def get_db_url(self) -> str:
		return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

	def get_redis_url(self) -> str:
		return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


@lru_cache
def settings() -> Settings:
	return Settings()
