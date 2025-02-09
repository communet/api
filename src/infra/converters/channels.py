from src.domain.entities.channels import Channel
from src.domain.values.channels import ChannelName
from src.infra.models.channels import ChannelModel


def convert_channel_model_to_entity(channel_model: ChannelModel) -> Channel:
    return Channel(
        oid=channel_model.oid,
        name=ChannelName(channel_model.name),
        description=channel_model.description,
        members=channel_model.profiles,
        is_deleted=channel_model.is_deleted,
        avatar=channel_model.avatar,
    )
