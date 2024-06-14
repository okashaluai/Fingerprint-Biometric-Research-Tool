import datetime

from Dev.DTOs import ExperimentDTO
from Dev.DataAccessLayer.DAOs import ExperimentDAO
from Dev.LogicLayer.LogicObjects.ILogicObject import ILogicObject


class Experiment(ILogicObject):
    def __init__(self, experiment_id, experiment_name):
        self.operations = list()
        self.experiment_id = experiment_id
        self.experiment_name = experiment_name
        self.experiment_date = datetime.datetime.now()

    def add_operation(self, operation):
        self.operations.append(operation)

    def remove_operation(self, operation):
        self.operations.remove(operation)

    def rename_experiment(self, new_experiment_name):
        self.experiment_name = new_experiment_name

    def to_dto(self) -> ExperimentDTO:
        return ExperimentDTO(operations=self.operations, experiment_id=self.experiment_id,
                             experiment_name=self.experiment_name, experiment_date=self.experiment_date)

    def to_dao(self) -> ExperimentDAO:
        raise NotImplementedError
