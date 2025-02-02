from abc import abstractmethod
from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select, update

from src.domain.entities.chanels import Chanel
from src.infra.models.chanels import ChanelModel
from src.infra.repositories.base import BaseRepository


@dataclass(eq=False, frozen=True)
class BaseChanelRepository(BaseRepository):
	@abstractmethod
	async def get_chanel_by_id(self, chanel_id: UUID) -> Chanel:
		...

	@abstractmethod
	async def delete_chanel_by_id(self, chanel_id: UUID) -> bool:
		...

	@abstractmethod
	async def create(self, chanel: Chanel) -> ChanelModel:
		...


@dataclass(eq=False, frozen=True)
class ChanelRepository(BaseChanelRepository):
	async def create(self, chanel: Chanel) -> ChanelModel:
		async with self._session as session:
			chanel_model = ChanelModel(
				oid=chanel.oid,
				name=chanel.name.as_generic_type(),
				description=chanel.description,
				avatar=chanel.avatar,
			)

			session.add(chanel_model)
			await session.commit()

	async def get_chanel_by_id(self, chanel_id: UUID) -> ChanelModel | None:
		async with self._session as session:
			stmt = select(ChanelModel).where(ChanelModel.oid == chanel_id)
			result = await session.execute(stmt)
			return result.scalar_one_or_none()

	async def delete_chanel_by_id(self, chanel_id: UUID) -> None:
		async with self._session as session:
			stmt = update(ChanelModel).where(ChanelModel.oid == chanel_id).values(is_deleted=True)
			await session.execute(stmt)
			await session.commit()
