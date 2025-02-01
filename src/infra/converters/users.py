from src.domain.entities.users import Credentials, Profile
from src.domain.values.users import Email, Username
from src.infra.models.users import CredentialsModel, ProfileModel


def convert_credentials_model_to_entity(credentials_model: CredentialsModel) -> Credentials:
	return Credentials(
		oid=credentials_model.oid,
		username=Username(credentials_model.username),
		email=Email(credentials_model.email),
		password=None,
	)


def convert_profile_model_to_entity(profile_model: ProfileModel) -> Profile:
	return Profile(
		oid=profile_model.oid,
		display_name=Username(profile_model.display_name),
		credentials=convert_credentials_model_to_entity(profile_model.credentials),
		avatar=profile_model.avatar,
	)
