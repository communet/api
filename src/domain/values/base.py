from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar


VT = TypeVar("VT")


@dataclass(frozen=True)
class BaseValue(ABC, Generic[VT]):
    """Base value object with common methods"""
    value: VT

    def __post_init__(self) -> None:
        """Calls after __init__ method"""
        self._validate()

    def as_generic_type(self) -> VT:
        """Return value as type which was specified in generic"""
        return self.value

    @abstractmethod
    def _validate(self) -> None:
        """Validate the field for correctness"""
        ...
