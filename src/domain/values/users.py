import bcrypt
import re

from dataclasses import dataclass

from src.domain.exceptions.users import (
    EmailEmptyException,
    PasswordEmptyException,
    UsernameEmptyException,
    EmailInvalidFormatException,
    PasswordTooShortException,
    UsernameTooLongException,
    UsernameTooShortException,
)
from src.domain.values.base import BaseValue


@dataclass(frozen=True)
class Username(BaseValue[str]):
    """
    Value object for username.
    :raises UsernameEmptyException: if the constructor gets an empty string or NoneType
    :raises UsernameTooShortException: if the constructor gets a short string (lt 3 chars by default)
    :raises UsernameTooLongException: if the constructor gets a long string (gt 20 chars by default)
    """
    def _validate(self) -> None:
        """This method will be calls in `__post_init__` method"""
        min_len, max_len = 3, 32

        if not self.value:
            raise UsernameEmptyException()
        if len(self.value) < min_len:
            raise UsernameTooShortException(min_len)
        if len(self.value) > max_len:
            raise UsernameTooLongException(max_len)


@dataclass(frozen=True)
class Email(BaseValue[str]):
    """
    Value object for email.
    :raises EmailEmptyException: if the constructor gets an empty string or NoneType
    :raises EmailInvalidFormatException: if the constructor gets an invalid format string
    """
    def _validate(self) -> None:
        """This method will be calls in `__post_init__` method"""
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"

        if not self.value:
            raise EmailEmptyException()

        if not re.fullmatch(pattern, self.value):
            raise EmailInvalidFormatException()


@dataclass(frozen=True)
class Password(BaseValue[str]):
    """
    Value object for password.
    :raises PasswordEmptyException: if the constructor gets an empty string or NoneType
    :raises PasswordTooShortException: if the constructor gets a short string (lt 8 chars by default)
    """
    def __post_init__(self) -> None:
        """validate and hash password after initializing"""
        self._validate(self.value)
        object.__setattr__(self, 'value', self._hash_password(self.value))

    def _hash_password(self, password: str) -> str:
        """:return: hashed password in string type"""
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")

    @staticmethod
    def check_passwords(password1: str, password2: str) -> bool:
        """
        Compare password and value of Password instance.
        :return: True if password and value are equal else False
        """
        return bcrypt.checkpw(password1.encode("utf-8"), password2.encode("utf-8"))

    def _validate(self, value: str) -> None:
        """This method will be calls in `__post_init__` method"""
        min_len = 8

        if not value:
            raise PasswordEmptyException()
        if len(value) <= min_len:
            raise PasswordTooShortException(min_len)
