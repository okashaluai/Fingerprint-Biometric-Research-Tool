from Dev.DTOs import OperationDTO
from Dev.DataAccessLayer.DAOs import OperationDAO
from Dev.LogicLayer.LogicObjects.ILogicObject import ILogicObject


class Operation(ILogicObject):
    def __init__(self):
        pass

    def to_dto(self) -> OperationDTO:
        raise NotImplementedError

    def to_dao(self) -> OperationDAO:
        raise NotImplementedError
