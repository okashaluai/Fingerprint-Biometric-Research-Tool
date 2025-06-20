from datetime import datetime
from Dev.DTOs import OperationDTO
from Dev.Enums import OperationType
from Dev.LogicLayer.LogicObjects.Asset import Asset
from Dev.LogicLayer.LogicObjects.ILogicObject import ILogicObject


class Operation(ILogicObject):
    def __init__(self, operation_id: str, operation_type: OperationType, operation_input: Asset,
                 operation_output: Asset | str, operation_datetime: datetime, operation_optional_extra_input: Asset | str = ''):
        self.operation_id: str = operation_id
        self.operation_type: OperationType = operation_type
        self.operation_input: Asset = operation_input
        self.operation_optional_extra_input: Asset | str = operation_optional_extra_input
        self.operation_output: Asset | str = operation_output
        self.operation_datetime: datetime = operation_datetime

    def to_dto(self) -> OperationDTO:
        return OperationDTO(operation_id=self.operation_id,
                            operation_type=self.operation_type,
                            operation_input=self.operation_input.to_dto(),
                            operation_output=self.operation_output.to_dto() if not isinstance(self.operation_output, str) else self.operation_output,
                            operation_datetime=self.operation_datetime,
                            operation_optional_extra_input= self.operation_optional_extra_input.to_dto() if not isinstance(self.operation_optional_extra_input, str) else self.operation_optional_extra_input)
