import datetime

from Dev.DTOs import ExperimentDTO
from Dev.DataAccessLayer.DAOs import ExperimentDAO
from Dev.Enums import OperationType
from Dev.LogicLayer.LogicObjects.Asset import Asset
from Dev.LogicLayer.LogicObjects.ILogicObject import ILogicObject
from Dev.LogicLayer.LogicObjects.Operation import Operation


class Experiment(ILogicObject):
    def __init__(self, experiment_id, experiment_name):
        self.operations = dict()
        self.experiment_id = experiment_id
        self.experiment_name = experiment_name
        self.experiment_date = datetime.datetime.now()
        self.next_operation_id = 1  # to be loaded from the DAL when it is implemented.

    def add_convert_operation(
            self,
            operation_type: OperationType,
            operation_input_path: str,
            operation_output_path: str
    ):
        input = Asset(operation_input_path)
        output = Asset(operation_output_path)
        operation = Operation(self.next_operation_id, operation_type, input, output)
        self.operations[self.next_operation_id] = operation
        return operation

    def remove_operation(self, operation_id: int):
        del self.operations[operation_id]

    def rename_experiment(self, new_experiment_name):
        self.experiment_name = new_experiment_name

    def to_dto(self) -> ExperimentDTO:
        return ExperimentDTO(operations=list(self.operations.values()), experiment_id=self.experiment_id,
                             experiment_name=self.experiment_name, experiment_date=self.experiment_date)

    def to_dao(self) -> ExperimentDAO:
        raise NotImplementedError
