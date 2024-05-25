import time
from abc import abstractmethod

from Dev.DTOs import AssetDTO
from Dev.DataAccessLayer.DAOs import AssetDAO
from Dev.LogicLayer.LogicObjects.ILogicObject import ILogicObject


class Asset(ILogicObject):
    def __init__(self, path: str):
        self.path = path
        self.date = time.time()  # TODO: this will be in the dal layer only.

    @abstractmethod
    def to_dto(self) -> AssetDTO:
        return AssetDTO(0, self.path, self.date)

    @abstractmethod
    def to_dao(self) -> AssetDAO:
        return AssetDAO()
