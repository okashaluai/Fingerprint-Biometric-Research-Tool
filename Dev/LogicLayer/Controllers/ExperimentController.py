from Dev.LogicLayer.LogicObjects.Experiment import Experiment
from Dev.LogicLayer.LogicObjects.Operation import Operation
from Dev.Utils import Singleton


class ExperimentController(metaclass=Singleton):

    def __init__(self):
        self.current_experiment_name = None
        self.experiments: dict[str, Experiment] = dict()  # <Key: experiment_name, Value: Experiment>

    def add_operation(self, operation: Operation) -> Operation:
        # TODO - need to save the added operation then return the new operation which contains the new input and
        #  output paths.
        return operation

    def get_experiments(self):
        return self.experiments

    def delete_experiment(self, experiment_name: str):
        raise NotImplementedError

    def export_experiment(self, experiment_name: int):
        raise NotImplementedError

    def rename_experiment(self, experiment_name: str, new_name: str):
        raise NotImplementedError

    def create_experiment(self, experiment_name: str):
        raise NotImplementedError

    def set_current_experiment(self, experiment_name: str):
        if experiment_name in self.experiments.keys():
            self.current_experiment_name = experiment_name
        else:
            raise Exception(f"Experiment with the name {experiment_name} doesn't exist!")
