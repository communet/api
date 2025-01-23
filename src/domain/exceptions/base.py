from dataclasses import dataclass


@dataclass(eq=False)
class ApplicationException(Exception):
    """Base exception for domain layer"""

    @property
    def message(self) -> str:
        return "Application exception was occurred"
