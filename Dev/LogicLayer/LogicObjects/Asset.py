from abc import abstractmethod

from Dev.DTOs import AssetDTO
from Dev.DataAccessLayer.DAOs import AssetDAO
from Dev.LogicLayer.LogicObjects.ILogicObject import ILogicObject


class Asset(ILogicObject):
    def __init__(self):
        pass

    @abstractmethod
    def to_dto(self) -> AssetDTO:
        raise NotImplementedError

    @abstractmethod
    def to_dao(self) -> AssetDAO:
        raise NotImplementedError
