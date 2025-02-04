from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar


@dataclass(frozen=True)
class BaseQuery(ABC):
    ...


QT = TypeVar('CT', bound=BaseQuery)
QR = TypeVar('CR', bound=Any)


@dataclass(frozen=True)
class BaseQueryHandler(Generic[QT, QR]):
    @abstractmethod
    async def handle(self, query: QT) -> QR:
        ...
