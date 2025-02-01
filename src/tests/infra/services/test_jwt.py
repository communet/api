import pytest

from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

from src.infra.services.jwt import BaseJWTService, JWTService
from src.infra.services.redis import BaseRedisService, RedisService
from src.settings.config import Settings, settings


@pytest.fixture
def redis_service() -> BaseRedisService:
	config = settings()
	return RedisService(config)


@pytest.fixture
def jwt_service() -> BaseJWTService:
	config = settings()
	return JWTService(config)


def test_generate_tokens(jwt_service, config: Settings = settings()) -> None:
	profile_id = str(uuid4())
	auth_data = jwt_service.generate_auth_tokens(profile_id)

	assert isinstance(auth_data.access_token, str)
	assert isinstance(auth_data.access_expires, datetime)
	assert auth_data.access_expires > datetime.now(timezone.utc)

	assert isinstance(auth_data.refresh_token, str)
	assert isinstance(auth_data.refresh_expires, timedelta)
	assert auth_data.refresh_expires.days == config.REFRESH_EXPIRES_IN_DAYS


def test_decode_jwt_token(jwt_service) -> None:
	profile_id = str(uuid4())
	jwt_token = jwt_service.generate_auth_tokens(profile_id).access_token
	profile_id_from_token = jwt_service.decode_jwt_token(jwt_token)

	assert profile_id_from_token is not None
	assert isinstance(profile_id_from_token, str)
	assert profile_id_from_token == profile_id
