from src.domain.entities.chanels import Chanel
from src.domain.values.chanels import ChanelName
from src.infra.models.chanels import ChanelModel


def convert_chanel_model_to_entity(chanel_model: ChanelModel) -> Chanel:
    return Chanel(
        oid=chanel_model.oid,
        name=ChanelName(chanel_model.name),
        description=chanel_model.description,
        is_deleted=chanel_model.is_deleted,
        avatar=chanel_model.avatar,
    )
