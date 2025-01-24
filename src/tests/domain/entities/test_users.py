import pytest
from src.domain.entities.users import Credentials, Profile
from src.domain.exceptions.base import ApplicationException
from src.domain.values.users import Email, Password, Username


def test_valid_credentials() -> None:
    username = "some_valid_username"
    email = "valid_email@gmail.com"
    password = "asdkfjaskldf"

    creds_from_init = Credentials(
        username=Username(username),
        email=Email(email),
        password=Password(password),
    )
    creds_from_factory = Credentials.create(
        username=username,
        email=email,
        password=password,
    )

    assert creds_from_init is not None
    assert creds_from_factory is not None

    assert creds_from_init != creds_from_factory
    assert creds_from_init.oid != creds_from_factory.oid
    assert creds_from_init.email == creds_from_factory.email
    assert creds_from_init.username == creds_from_factory.username


def test_invalid_credentials() -> None:
    invalid_test_cases = (
        {
            "username": "12",
            "email": "ankitrai326.com",
            "password": "some_password",
        },
        {
            "username": "valid_email@mail.ru",
            "email": "ankitrai326.com",
            "password": None,
        },
        {
            "username": None,
            "email": "ankitrai326.com",
            "password": "",
        },
    )

    for test_case in invalid_test_cases:
        with pytest.raises(ApplicationException):
            Credentials.create(
                username=test_case.get("username", None),
                email=test_case.get("email"),
                password=test_case.get("password"),
            )


def test_valid_profile() -> None:
    creds = Credentials.create("username", "asdfasdfasf@gmail.com", "askdfasdf")
    display_name = Username("valid_display_name")
    avatar = "asdfasdfasdf.jpg"

    profile_from_init = Profile(
        display_name=display_name,
        avatar=avatar,
        credentials=creds,
    )
    profile_from_factory = Profile.create(
        display_name="valid_display_name",
        avatar=avatar,
        credentials=creds,
    )

    assert profile_from_init is not None
    assert profile_from_factory is not None

    assert profile_from_init != profile_from_factory
    assert profile_from_init.oid != profile_from_factory.oid
    assert profile_from_init.avatar == profile_from_factory.avatar
    assert profile_from_init.credentials == profile_from_factory.credentials


def test_invalid_profile() -> None:
    creds = Credentials.create("username", "asdfasdfasf@gmail.com", "askdfasdf")
    invalid_test_cases = ("as", "s"*33)

    for test_case in invalid_test_cases:
        with pytest.raises(ApplicationException):
            Profile.create(
                display_name=test_case,
                avatar="asdf",
                credentials=creds,
            )
