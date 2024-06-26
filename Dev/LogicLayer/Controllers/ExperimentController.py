from Dev.Enums import OperationType
from Dev.LogicLayer.LogicObjects.Experiment import Experiment
from Dev.Utils import Singleton


class ExperimentController(metaclass=Singleton):

    def __init__(self):
        self.current_experiment_id = None
        self.next_experiment_id = 1  # to be loaded from the DAL when it is implemented.
        self.experiments: dict[int, Experiment] = dict()  # <Key: experiment_id, Value: Experiment>

    def add_operation(
            self,
            operation_type: OperationType,
            operation_input_path: str,
            operation_output_path: str
    ):
        return self.experiments[self.current_experiment_id].add_convert_operation(operation_type,
                                                                                       operation_input_path,
                                                                                       operation_output_path)

    def get_experiments(self):
        return self.experiments.values()

    def delete_experiment(self, experiment_id: int):
        if experiment_id in self.experiments:
            del self.experiments[experiment_id]
        else:
            raise Exception(f'Experiment with id {experiment_id} does not exist!')

    def get_sorted_experiments_by_date(self):
        return sorted(self.experiments.values(), key=lambda experiment: experiment.experiment_date)

    def export_experiment(self, experiment_id: int, export_path: str):
        raise NotImplementedError

    def load_experiments(self):
        raise NotImplementedError

    def rename_experiment(self, experiment_id: int, new_experiment_name: str):
        if experiment_id in self.experiments:
            self.experiments[experiment_id].rename_experiment(new_experiment_name)
            return self.experiments[experiment_id]
        else:
            raise Exception(f'Experiment with id {experiment_id} does not exist!')

    def create_experiment(self, experiment_name: str):
        for experiment in self.experiments.values():
            if experiment.experiment_name == experiment_name:
                raise Exception(f'Experiment with name {experiment_name} already exist!')

        new_experiment_id = self.next_experiment_id
        self.next_experiment_id += 1

        new_experiment = Experiment(new_experiment_id, experiment_name)
        self.experiments[new_experiment_id] = new_experiment

        return self.experiments[new_experiment_id]

    def set_current_experiment(self, current_experiment_id: int):
        if current_experiment_id in self.experiments:
            self.current_experiment_id = current_experiment_id
            return self.experiments[self.current_experiment_id]
        else:
            raise Exception(f'Experiment with id {current_experiment_id} does not exist!')

    def get_current_experiment(self):
        if self.current_experiment_id in self.experiments:
            return self.experiments[self.current_experiment_id]
        else:
            raise Exception(f'Experiment with id {self.current_experiment_id} does not exist!')

    def delete_operation(self, experiment_id: int, operation_id: int):
        if experiment_id not in self.experiments.keys():
            raise Exception(f'Experiment with id {self.current_experiment_id} does not exist!')
        if operation_id not in self.experiments[experiment_id].operations.keys():
            raise Exception(f'Operation with id {self.current_experiment_id} does not exist!')
        else:
            self.experiments[experiment_id].remove_operation(operation_id)
