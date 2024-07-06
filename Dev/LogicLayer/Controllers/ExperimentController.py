import os

from Dev.Enums import OperationType
from Dev.LogicLayer.LogicObjects.Experiment import Experiment
from Dev.LogicLayer.LogicObjects.Operation import Operation
from Dev.Utils import Singleton
from Dev.Playground import PLAYGROUND


class ExperimentController(metaclass=Singleton):

    def __init__(self):
        self.current_experiment_name = None
        self.experiments: dict[str, Experiment] = dict()  # <Key: experiment_name, Value: Experiment>
        self.playground: PLAYGROUND = PLAYGROUND()

    def add_operation(self, operation: Operation):

        return self.experiments[self.current_experiment_name].add_convert_operation(operation)

    def get_experiments(self):
        return self.experiments.values()

    def delete_experiment(self, experiment_name: str):
        if experiment_name in self.experiments:
            del self.experiments[experiment_name]
        else:
            raise Exception(f'Experiment with name {experiment_name} does not exist!')

    def get_sorted_experiments_by_date(self):
        return sorted(self.experiments.values(), key=lambda experiment: experiment.experiment_date)

    def export_experiment(self, experiment_name: str, export_path: str):
        raise NotImplementedError

    def load_experiments(self):
        raise NotImplementedError

    def rename_experiment(self, experiment_name: str, new_experiment_name: str):
        if experiment_name in self.experiments:
            self.experiments[experiment_name].rename_experiment(new_experiment_name)
            return self.experiments[experiment_name]
        else:
            raise Exception(f'Experiment with name {experiment_name} does not exist!')

    def create_experiment(self, experiment_name: str):

        if experiment_name in self.experiments:
            raise Exception(f'Experiment with name {experiment_name} already exists!')

        self.playground.create_experiment_dir(experiment_name=experiment_name)

        new_experiment = Experiment(experiment_name)
        self.experiments[experiment_name] = new_experiment

        return self.experiments[experiment_name]

    def set_current_experiment(self, current_experiment_name: str) -> Experiment:
        if current_experiment_name in self.experiments:
            self.current_experiment_name = current_experiment_name
            return self.experiments[self.current_experiment_name]
        else:
            raise Exception(f'Experiment with name {current_experiment_name} does not exist!')

    def import_templates(self, templates_path: str, operation_id: str):
        experiment_name = self.experiments.get(self.current_experiment_name).experiment_name

        if os.path.isfile(templates_path):
            self.playground.import_template_into_dir(templates_path, experiment_name, operation_id)
        elif os.path.isdir(templates_path):
            self.playground.import_templates_dir(templates_path, experiment_name, operation_id)

        else:
            raise Exception(f"{templates_path} does not exist or is not a valid path.")

    def import_images(self, images_path: str, operation_id: str):
        experiment_name = self.experiments.get(self.current_experiment_name).experiment_name
        if os.path.isfile(images_path):
            self.playground.import_image_into_dir(images_path, experiment_name, operation_id)
        elif os.path.isdir(images_path):
            self.playground.import_images_dir(images_path, experiment_name, operation_id)
        else:
            raise Exception(f"{images_path} does not exist or is not a valid path.")

    def get_current_experiment(self) -> Experiment:
        if self.current_experiment_name in self.experiments:
            return self.experiments[self.current_experiment_name]
        else:
            raise Exception(f'There is no current experiment!')

    def delete_operation(self, experiment_name: str, operation_id: str):
        if experiment_name not in self.experiments.keys():
            raise Exception(f'Experiment with name {self.current_experiment_name} does not exist!')
        if operation_id not in self.experiments[experiment_name].operations.keys():
            raise Exception(f'Operation with id {self.current_experiment_name} does not exist!')
        else:
            self.experiments[experiment_name].remove_operation(operation_id)
