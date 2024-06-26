import time
from abc import abstractmethod
from datetime import datetime

from Dev.DTOs import AssetDTO
from Dev.DataAccessLayer.DAOs import AssetDAO
from Dev.LogicLayer.LogicObjects.ILogicObject import ILogicObject


class Asset(ILogicObject):
    def __init__(self, path: str):
        self.path = path
        self.date = datetime.now()  # TODO: this will be in the dal layer only.

    def to_dto(self) -> AssetDTO:
        return AssetDTO(0, self.path, self.date)

    def to_dao(self) -> AssetDAO:
        # return AssetDAO()
        raise NotImplementedError
