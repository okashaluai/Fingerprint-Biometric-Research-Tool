from datetime import datetime
from Dev.DTOs import ExperimentDTO
from Dev.LogicLayer.LogicObjects.ILogicObject import ILogicObject
from Dev.LogicLayer.LogicObjects.Operation import Operation


class Experiment(ILogicObject):
    def __init__(self, experiment_name, experiment_datetime: datetime, experiment_last_update_date: datetime, operations: dict[str: Operation] = None):
        if experiment_name is None:
            raise Exception('Experiment name cannot be None')
        if len(experiment_name) < 1 or len(experiment_name) > 20:
            raise Exception('Experiment name must be between 1 and 20 characters')

        if operations is None:
            self.operations: dict[str: Operation] = dict()
        else:
            self.operations: dict[str: Operation] = operations

        self.experiment_name: str = experiment_name
        self.experiment_datetime: datetime = experiment_datetime
        self.experiment_last_update_date = experiment_last_update_date
    def add_convert_operation(
            self,
            operation: Operation,
    ):
        self.operations[operation.operation_id] = operation
        return operation

    def remove_operation(self, operation_id: str):
        del self.operations[operation_id]

    def rename_experiment(self, new_experiment_name):
        if new_experiment_name is None:
            raise Exception('Experiment name cannot be None')
        if len(new_experiment_name) < 1 or len(new_experiment_name) > 20:
            raise Exception('Experiment name must be between 1 and 20 characters')

        self.experiment_name = new_experiment_name

    def to_dto(self) -> ExperimentDTO:
        operation_dtos = list()
        for operation in self.operations.values():
            operation_dto = operation.to_dto()
            operation_dtos.append(operation_dto)

        return ExperimentDTO(operations=operation_dtos,
                             experiment_name=self.experiment_name,
                             experiment_datetime=self.experiment_datetime,
                             experiment_last_update_date=self.experiment_last_update_date)
