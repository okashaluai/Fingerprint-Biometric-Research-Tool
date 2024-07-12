import datetime

from Dev.DTOs import ExperimentDTO
from Dev.DataAccessLayer.DAOs import ExperimentDAO
from Dev.Enums import OperationType
from Dev.LogicLayer.LogicObjects.Asset import Asset
from Dev.LogicLayer.LogicObjects.ILogicObject import ILogicObject
from Dev.LogicLayer.LogicObjects.Operation import Operation


class Experiment(ILogicObject):
    def __init__(self, experiment_name):
        if experiment_name is None:
            raise Exception('Experiment name cannot be None')
        if len(experiment_name) < 1 or len(experiment_name) > 20:
            raise Exception('Experiment name must be between 1 and 20 characters')

        self.operations: dict[str: Operation] = dict()
        self.experiment_name: str = experiment_name
        self.experiment_date = datetime.datetime.now()

    def add_convert_operation(
            self,
            operation: Operation,
    ):
        self.operations[operation.operation_id] = operation
        return operation

    def remove_operation(self, operation_id: str):
        del self.operations[operation_id]

    def rename_experiment(self, new_experiment_name):
        self.experiment_name = new_experiment_name

    def to_dto(self) -> ExperimentDTO:
        return ExperimentDTO(operations=list(self.operations.values()),
                             experiment_name=self.experiment_name, experiment_date=self.experiment_date)

    def to_dao(self) -> ExperimentDAO:
        raise NotImplementedError
