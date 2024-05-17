from abc import abstractmethod
from Dev.DTOs import AssetDTO
from Dev.DataAccessLayer.DAOs import AssetDAO
from Dev.LogicLayer.LogicObjects.ILogicObject import ILogicObject
from datetime import datetime

class Asset(ILogicObject):
    def __init__(self, path):
        self.__path = path
        self.__date = datetime.now()

    @abstractmethod
    def to_dto(self) -> AssetDTO:
        return AssetDTO(0, self.__path, self.__date)

    @abstractmethod
    def to_dao(self) -> AssetDAO:
        return AssetDAO()
