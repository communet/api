from abc import ABC, abstractmethod

from pydantic import BaseModel

from src.domain.entities.base import BaseEntity


class BaseRequestSchema(ABC, BaseModel):
    ...


class BaseResponseSchema(ABC, BaseModel):
    @classmethod
    @abstractmethod
    def from_entity(cls, entity: BaseEntity) -> "BaseResponseSchema":
        """Convert entity to response schema."""
        ...


class ErrorSchema(BaseModel):
    """Base error schema for response"""
    error: str
