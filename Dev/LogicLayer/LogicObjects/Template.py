from Dev.DTOs import TemplateDTO
from Dev.DataAccessLayer.DAOs import TemplateDAO
from Dev.LogicLayer.LogicObjects.Asset import Asset
from Dev.LogicLayer.LogicObjects.ILogicObject import ILogicObject


class Template(Asset):
    def __init__(self):
        super().__init__()

    def to_dto(self) -> TemplateDTO:
        raise NotImplementedError

    def to_dao(self) -> TemplateDAO:
        raise NotImplementedError
