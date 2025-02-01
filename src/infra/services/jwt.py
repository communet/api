import jwt

from abc import ABC
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from src.domain.entities.users import AuthData
from src.settings.config import Settings


class BaseJWTService(ABC):
	def generate_auth_tokens(self, profile_id: str) -> AuthData:
		...

	def decode_jwt_token(self, token: str) -> str | None:
		...


class JWTService(BaseJWTService):
	def __init__(self, config: Settings) -> None:
		self.__config: Settings = config

	def decode_jwt_token(self, token: str) -> str | None:
		try:
			payload = jwt.decode(
				jwt=token,
				key=self.__config.API_SECRET,
				algorithms=["HS256"],
			)
		except jwt.InvalidTokenError:
			return None

		expire = payload.get("exp")
		expire_time = datetime.fromtimestamp(int(expire), timezone.utc)
		if (not expire) or (expire_time < datetime.now(timezone.utc)):
			return None

		profile_id = payload.get("sub")
		if not profile_id:
			return None

		return profile_id


	def generate_auth_tokens(self, profile_id: str) -> AuthData:
		access_token, access_expires = self.__generate_access_token(profile_id)
		refresh_token, refresh_expires = self.__generate_refresh_token()

		return AuthData(
			access_token=access_token,
			access_expires=access_expires,
			refresh_token=refresh_token,
			refresh_expires=refresh_expires,
		)

	def __generate_access_token(self, profile_id: str) -> tuple[str, datetime]:
		access_expires = datetime.now(timezone.utc) + timedelta(minutes=self.__config.JWT_EXPIRES_IN_MINUTES)
		access_token = jwt.encode(
			payload={
				"sub": profile_id,
				"exp": access_expires,
			},
			key=self.__config.API_SECRET,
			algorithm="HS256",
		)

		return access_token, access_expires

	def __generate_refresh_token(self) -> tuple[str, timedelta]:
		refresh_token = str(uuid4())
		refresh_expires = timedelta(days=self.__config.REFRESH_EXPIRES_IN_DAYS)

		return refresh_token, refresh_expires
