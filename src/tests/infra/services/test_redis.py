import pytest

from datetime import timedelta

from src.infra.services.redis import RedisService
from src.settings.config import settings


pytest_plugin = ("pytest_asyncio")


@pytest.fixture
def redis_service() -> RedisService:
	config = settings()
	return RedisService(config)


@pytest.mark.asyncio
async def test_set_value(redis_service) -> None:
	test_data = {"key": "test_key", "value": "test_value", "ttl": timedelta(minutes=2)}

	result = await redis_service.set(
		key=test_data.get("key"),
		value=test_data.get("value"),
		ttl=test_data.get("ttl"),
	)

	assert result is True


@pytest.mark.asyncio
async def test_get_value(redis_service):
	invalid_key = "asdfasdfsafd"
	valid_data = {
		"key": "test_key",
		"expected_value": "test_value",
	}

	result = await redis_service.get(valid_data.get("key"))
	assert result == valid_data.get("expected_value")

	result = await redis_service.get(invalid_key)
	assert result is None


@pytest.mark.asyncio
async def test_delete_value(redis_service):
	valid_key = "test_key"
	invalid_key = "asdkfjaskdfjaslfdk"

	result = await redis_service.delete(valid_key)
	assert result is True

	result = await redis_service.delete(invalid_key)
	assert result is False
