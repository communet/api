from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Optional

from redis.asyncio import Redis

from src.settings.config import Settings


class BaseRedisService(ABC):
	@abstractmethod
	async def get(self, key: str) -> Optional[str]:
		...

	@abstractmethod
	async def set(self, key: str, value: str, ttl: timedelta) -> bool:
		...

	@abstractmethod
	async def delete(self, key: str) -> bool:
		...

	@abstractmethod
	async def pop(self, key: str) -> Optional[str]:
		...


class RedisService(BaseRedisService):
	def __init__(self, config: Settings) -> None:
		self.__config: Settings = config
		self.__client: Redis = Redis.from_url(url=self.__config.get_redis_url())

	async def get(self, key: str) -> Optional[str]:
		result = await self.__client.get(name=key)
		if result:
			result = result.decode("utf-8")
		return result

	async def set(self, key: str, value: str, ttl: timedelta) -> bool:
		return await self.__client.set(
			name=key,
			value=value,
			ex=ttl,
		)

	async def pop(self, key: str) -> Optional[str]:
		result = await self.get(key=key)
		if result:
			await self.delete(key=key)
		return result

	async def delete(self, key: str) -> bool:
		result = await self.__client.delete(key)
		return bool(result)
