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

	def get_db_url(self) -> str:
		return f'postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'


@lru_cache
def get_settings() -> Settings:
	return Settings()
