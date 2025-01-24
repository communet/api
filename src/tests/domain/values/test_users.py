import pytest

from src.domain.exceptions.users import (
    EmailInvalidFormatException,
    EmailEmptyException,
    PasswordEmptyException,
    UsernameEmptyException,
    UsernameTooLongException,
    UsernameTooShortException,
    PasswordTooShortException,
)
from src.domain.values.users import Email, Password, Username


def test_valid_username() -> None:
    valid_cases = ["123", "some_valid_username", "a"*32]

    for test_case in valid_cases:
        username = Username(test_case)

        assert isinstance(username.as_generic_type(), str)
        assert username.as_generic_type() is not None
        assert username.as_generic_type() == test_case


def test_invalid_username() -> None:
    short_username = "12"
    long_username = "a" * 33
    empty_username = None

    with pytest.raises(UsernameEmptyException):
        Username(empty_username)

    with pytest.raises(UsernameTooShortException):
        Username(short_username)

    with pytest.raises(UsernameTooLongException):
        Username(long_username)

def test_valid_email() -> None:
    test_cases = [
        "ankitrai326@gmail.com",
        "my.ownsite@our-earth.org",
    ]

    for test_case in test_cases:
        email = Email(test_case)
        assert email.as_generic_type() == test_case


def test_invalid_email() -> None:
    invalid_format_email = "ankitrai326.com"
    empty_emails = ("", None)

    with pytest.raises(EmailInvalidFormatException):
        Email(invalid_format_email)

    for email in empty_emails:
        with pytest.raises(EmailEmptyException):
            Email(email)


def test_valid_password() -> None:
    valid_password = "some_valid_password"
    password = Password(valid_password)

    assert password.value != valid_password
    assert isinstance(password.value, str)
    assert password.check_password(valid_password) is True


def test_invalid_password() -> None:
    valid_password = "some_password"
    invalid_password = "incorrect_password"
    short_password = "123"
    empty_passwords = ("", None)

    with pytest.raises(PasswordTooShortException):
        Password(short_password)

    for password in empty_passwords:
        with pytest.raises(PasswordEmptyException):
            Password(password)

    password = Password(valid_password)
    assert password.check_password(invalid_password) is False
