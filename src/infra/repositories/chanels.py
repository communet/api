from abc import abstractmethod
from dataclasses import dataclass

from src.domain.entities.chanels import Chanel
from src.infra.models.chanels import ChanelModel
from src.infra.repositories.base import BaseRepository


@dataclass(eq=False, frozen=True)
class BaseChanelRepository(BaseRepository):
	@abstractmethod
	async def create(self, chanel: Chanel) -> ChanelModel:
		...


@dataclass(eq=False, frozen=True)
class ChanelRepository(BaseChanelRepository):
	async def create(self, chanel: Chanel) -> ChanelModel:
		async with self._session:
			chanel_model = ChanelModel(
				oid=chanel.oid,
				name=chanel.name.as_generic_type(),
				description=chanel.description,
				avatar=chanel.avatar,
			)

			self._session.add(chanel_model)
			await self._session.commit()
