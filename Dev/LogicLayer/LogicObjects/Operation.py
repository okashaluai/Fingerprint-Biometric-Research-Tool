import time

from Dev.DTOs import OperationDTO
from Dev.DataAccessLayer.DAOs import OperationDAO
from Dev.Enums import OperationType
from Dev.LogicLayer.LogicObjects.Asset import Asset
from Dev.LogicLayer.LogicObjects.ILogicObject import ILogicObject


class Operation(ILogicObject):
    def __init__(self, experiment_name: str, operation_type: OperationType, input: Asset, output: Asset):
        self.experiment_name = experiment_name
        self.operation_type = operation_type
        self.input = input
        self.output = output
        self.date = time.time()

    def to_dto(self) -> OperationDTO:
        raise NotImplementedError

    def to_dao(self) -> OperationDAO:
        raise NotImplementedError
