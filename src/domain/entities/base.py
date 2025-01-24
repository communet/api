from abc import ABC
from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class BaseEntity(ABC):
    """Base entity with common attributes and methods"""
    oid: UUID = field(
        default_factory=uuid4,
        kw_only=True,
    )

    # TODO: add methods for register and pool events here

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, __value: 'BaseEntity') -> bool:
        return self.oid == __value.oid
