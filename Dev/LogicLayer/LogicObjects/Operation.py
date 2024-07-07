from datetime import datetime
from Dev.DTOs import OperationDTO
from Dev.DataAccessLayer.DAOs import OperationDAO
from Dev.Enums import OperationType
from Dev.LogicLayer.LogicObjects.Asset import Asset
from Dev.LogicLayer.LogicObjects.ILogicObject import ILogicObject


class Operation(ILogicObject):
    def __init__(self, operation_id: str, operation_type: OperationType, operation_input: Asset,
                 operation_output: Asset):
        self.operation_id = operation_id
        self.operation_type = operation_type
        self.operation_input = operation_input
        self.operation_output = operation_output
        self.operation_date = datetime.now()

    def to_dto(self) -> OperationDTO:
        return OperationDTO(operation_id=self.operation_id, operation_type=self.operation_type,
                            operation_input=self.operation_input.to_dto(),
                            operation_output=self.operation_output.to_dto(),
                            operation_date=self.operation_date)

    def to_dao(self) -> OperationDAO:
        raise NotImplementedError
