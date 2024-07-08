import os
import shutil


class PLAYGROUND:
    def __init__(self):
        self.PATH = os.curdir
        self.temp_dir = os.path.join(self.PATH, 'temp_dir')

    def create_experiment_dir(self, experiment_name: str) -> str:
        experiment_dir_path = os.path.join(self.PATH, experiment_name)
        os.makedirs(experiment_dir_path, exist_ok=True)
        return experiment_dir_path

    def prepare_template_to_image_operation_dir(self, experiment_name: str, operation_id: str):
        experiment_dir_path = os.path.join(self.PATH, experiment_name)
        operation_dir_path = os.path.join(experiment_dir_path, operation_id)
        if os.path.exists(experiment_dir_path) and os.path.isdir(experiment_dir_path):
            os.makedirs(operation_dir_path, exist_ok=True)

            min_maps_dir = os.path.join(operation_dir_path, 'min_maps')
            os.makedirs(min_maps_dir, exist_ok=True)

            templates_dir = os.path.join(operation_dir_path, 'templates')
            os.makedirs(templates_dir, exist_ok=True)

            images_dir = os.path.join(operation_dir_path, 'images')
            os.makedirs(images_dir, exist_ok=True)
        else:
            raise Exception(f'Experiment directory {experiment_name} does not exist')

        return operation_dir_path

    def prepare_image_to_template_operation_dir(self, experiment_name: str, operation_id: str):
        experiment_dir_path = os.path.join(self.PATH, experiment_name)
        operation_dir_path = os.path.join(experiment_dir_path, operation_id)
        if os.path.exists(experiment_dir_path) and os.path.isdir(experiment_dir_path):
            os.makedirs(operation_dir_path, exist_ok=True)

            templates_dir = os.path.join(operation_dir_path, 'templates')
            os.makedirs(templates_dir, exist_ok=True)

            images_dir = os.path.join(operation_dir_path, 'images')
            os.makedirs(images_dir, exist_ok=True)
        else:
            raise Exception(f'Experiment directory {experiment_name} does not exist')

        return operation_dir_path

    def prepare_image_to_printing_object_operation_dir(self, experiment_name: str, operation_id: str):
        experiment_dir_path = os.path.join(self.PATH, experiment_name)
        operation_dir_path = os.path.join(experiment_dir_path, operation_id)
        if os.path.exists(experiment_dir_path) and os.path.isdir(experiment_dir_path):
            os.makedirs(operation_dir_path, exist_ok=True)

            images_dir = os.path.join(operation_dir_path, 'images')
            os.makedirs(images_dir, exist_ok=True)

            printing_objects_dir = os.path.join(operation_dir_path, 'printing_objects')
            os.makedirs(printing_objects_dir, exist_ok=True)
        else:
            raise Exception(f'Experiment directory {experiment_name} does not exist')

        return operation_dir_path

    def get_sub_templates_dir_path(self, experiment_name: str, operation_id: str) -> str:
        experiment_dir_path = os.path.join(self.PATH, experiment_name)
        operation_dir_path = os.path.join(experiment_dir_path, operation_id)
        if os.path.exists(experiment_dir_path) and os.path.isdir(experiment_dir_path):
            if os.path.exists(operation_dir_path) and os.path.isdir(operation_dir_path):
                return os.path.join(operation_dir_path, 'templates')
            else:
                raise Exception(f'Operation directory {operation_id} does not exist')
        else:
            raise Exception(f'Experiment directory {experiment_name} does not exist')

    def get_sub_images_dir_path(self, experiment_name: str, operation_id: str) -> str:
        experiment_dir_path = os.path.join(self.PATH, experiment_name)
        operation_dir_path = os.path.join(experiment_dir_path, operation_id)
        if os.path.exists(experiment_dir_path) and os.path.isdir(experiment_dir_path):
            if os.path.exists(operation_dir_path) and os.path.isdir(operation_dir_path):
                return os.path.join(operation_dir_path, 'images')
            else:
                raise Exception(f'Operation directory {operation_id} does not exist')
        else:
            raise Exception(f'Experiment directory {experiment_name} does not exist')

    def get_sub_min_maps_dir_path(self, experiment_name: str, operation_id: str) -> str:
        experiment_dir_path = os.path.join(self.PATH, experiment_name)
        operation_dir_path = os.path.join(experiment_dir_path, operation_id)
        if os.path.exists(experiment_dir_path) and os.path.isdir(experiment_dir_path):
            if os.path.exists(operation_dir_path) and os.path.isdir(operation_dir_path):
                return os.path.join(operation_dir_path, 'min_maps')
            else:
                raise Exception(f'Operation directory {operation_id} does not exist')
        else:
            raise Exception(f'Experiment directory {experiment_name} does not exist')

    def get_sub_printing_objects_dir_path(self, experiment_name: str, operation_id: str) -> str:
        experiment_dir_path = os.path.join(self.PATH, experiment_name)
        operation_dir_path = os.path.join(experiment_dir_path, operation_id)
        if os.path.exists(experiment_dir_path) and os.path.isdir(experiment_dir_path):
            if os.path.exists(operation_dir_path) and os.path.isdir(operation_dir_path):
                return os.path.join(operation_dir_path, 'printing_objects')
            else:
                raise Exception(f'Operation directory {operation_id} does not exist')
        else:
            raise Exception(f'Experiment directory {experiment_name} does not exist')

    def get_temp_dir_path(self):
        if not (os.path.exists(self.temp_dir) and os.path.isdir(self.temp_dir)):
            os.makedirs(self.temp_dir)
        return self.temp_dir

    def get_temp_min_maps_dir_path(self):
        temp_dir_path = self.get_temp_dir_path()
        temp_min_maps_dir_path = os.path.join(temp_dir_path, 'temp_min_maps')
        if not (os.path.exists(temp_min_maps_dir_path) and os.path.isdir(temp_min_maps_dir_path)):
            os.makedirs(temp_min_maps_dir_path)
        return temp_min_maps_dir_path

    def import_temp_template(self, template_path):
        if not os.path.exists(template_path):
            raise Exception(f'Template path {template_path} does not exist')
        temp_dir_path = self.get_temp_dir_path()
        shutil.copy(template_path, temp_dir_path)
        return os.path.join(temp_dir_path, os.path.basename(template_path))

    def import_template_into_dir(self, templates_path: str, experiment_name: str, operation_id: str) -> str:
        experiment_dir_path = os.path.join(self.PATH, experiment_name)
        operation_dir_path = os.path.join(experiment_dir_path, operation_id)
        template_name = os.path.basename(templates_path)
        if os.path.exists(experiment_dir_path) and os.path.isdir(experiment_dir_path):
            if os.path.exists(operation_dir_path) and os.path.isdir(operation_dir_path):
                dest_dir_path = os.path.join(self.get_sub_templates_dir_path(experiment_name, operation_id),
                                             template_name)
                shutil.copy(templates_path, dest_dir_path)
            else:
                raise Exception(f'Operation directory {operation_id} does not exist')
        else:
            raise Exception(f'Experiment directory {experiment_name} does not exist')
        return dest_dir_path

    def import_templates_dir(self, templates_path: str, experiment_name: str, operation_id: str) -> str:
        experiment_dir_path = os.path.join(self.PATH, experiment_name)
        operation_dir_path = os.path.join(experiment_dir_path, operation_id)
        if os.path.exists(experiment_dir_path) and os.path.isdir(experiment_dir_path):
            if os.path.exists(operation_dir_path) and os.path.isdir(operation_dir_path):
                dest_dir_path = self.get_sub_templates_dir_path(experiment_name, operation_id)
                shutil.copytree(templates_path, dest_dir_path, dirs_exist_ok=True)
            else:
                raise Exception(f'Operation directory {operation_id} does not exist')
        else:
            raise Exception(f'Experiment directory {experiment_name} does not exist')
        return dest_dir_path

    def import_image_into_dir(self, images_path: str, experiment_name: str, operation_id: str) -> str:
        experiment_dir_path = os.path.join(self.PATH, experiment_name)
        operation_dir_path = os.path.join(experiment_dir_path, operation_id)
        image_name = os.path.basename(images_path)

        if os.path.exists(experiment_dir_path) and os.path.isdir(experiment_dir_path):
            if os.path.exists(operation_dir_path) and os.path.isdir(operation_dir_path):
                dest_dir_path = os.path.join(self.get_sub_images_dir_path(experiment_name, operation_id),
                                             image_name)
                shutil.copy(images_path, dest_dir_path)
            else:
                raise Exception(f'Operation directory {operation_id} does not exist')
        else:
            raise Exception(f'Experiment directory {experiment_name} does not exist')
        return dest_dir_path

    def import_images_dir(self, images_path: str, experiment_name: str, operation_id: str) -> str:
        experiment_dir_path = os.path.join(self.PATH, experiment_name)
        operation_dir_path = os.path.join(experiment_dir_path, operation_id)

        if os.path.exists(experiment_dir_path) and os.path.isdir(experiment_dir_path):
            if os.path.exists(operation_dir_path) and os.path.isdir(operation_dir_path):
                dest_dir_path = self.get_sub_images_dir_path(experiment_name, operation_id)
                shutil.copytree(images_path, dest_dir_path, dirs_exist_ok=True)
            else:
                raise Exception(f'Operation directory {operation_id} does not exist')
        else:
            raise Exception(f'Experiment directory {experiment_name} does not exist')
        return dest_dir_path


