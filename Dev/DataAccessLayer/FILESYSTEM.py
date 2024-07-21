import os
import shutil
import json
from Dev.DTOs import ExperimentDTO, OperationDTO, ImageDTO, TemplateDTO, PrintingObjectDTO, AssetDTO
from datetime import datetime
from Dev.Enums import OperationType
from Dev.Utils import Singleton
from pathlib import Path


class FILESYSTEM(metaclass=Singleton):
    def __init__(self):
        self.experiments_home_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'experiments'))
        self.temp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'temp_dir'))
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def load_experiments(self):
        if not (os.path.exists(self.experiments_home_path) and os.path.isdir(self.experiments_home_path)):
            os.mkdir(self.experiments_home_path)
        experiments: list[ExperimentDTO] = list()

        experiments_dirs = os.listdir(self.experiments_home_path)
        for experiment_dir in experiments_dirs:
            experiment_dto = self.load_experiment(experiment_dir)
            experiments.append(experiment_dto)

        # if not (os.path.exists(self.temp_dir) and os.path.isdir(self.temp_dir)):
        #     os.mkdir(self.temp_dir)

        return experiments

    def load_experiment(self, experiment_name: str) -> ExperimentDTO:
        experiment_path = os.path.join(self.experiments_home_path, experiment_name)
        if not os.path.isdir(experiment_path):
            raise Exception(f'Experiment {experiment_name} does not exist')
        operations_dirs = os.listdir(experiment_path)

        operations: list[OperationDTO] = list()
        for operation_dir in operations_dirs:
            operation_dto = self.load_operation(experiment_name, operation_dir)
            operations.append(operation_dto)
        # creation_date = os.stat(experiment_path).st_ctime
        latest_update_date = datetime.fromtimestamp(os.stat(experiment_path).st_mtime)
        experiment_dto = ExperimentDTO(experiment_name=experiment_name,
                                       experiment_datetime=latest_update_date,
                                       operations=operations)
        return experiment_dto

    def load_operation(self, experiment_name: str, operation_id: str) -> OperationDTO:
        operation_path = os.path.join(self.experiments_home_path, experiment_name, operation_id)
        if not os.path.isdir(operation_path):
            raise Exception(f'Operation {operation_path} does not exist')

        operation_metadata = self.load_operation_metadata(experiment_name, operation_id)
        operation_type = OperationType(operation_metadata['operation_type'])
        operation_datetime = datetime.fromtimestamp(float(operation_metadata['operation_timestamp']))
        operation_input = self.wrap_asset(operation_metadata['input_asset_path'])
        operation_output = self.wrap_asset(operation_metadata['output_asset_path'])
        operation_extra_optional_input = self.wrap_asset(operation_metadata['optional_extra_asset_path'])

        operation_dto = OperationDTO(operation_id=operation_id,
                                     operation_datetime=operation_datetime,
                                     operation_type=operation_type,
                                     operation_input=operation_input,
                                     operation_output=operation_output,
                                     operation_optional_extra_input=operation_extra_optional_input)
        return operation_dto

    def wrap_asset(self, asset_path: str) -> AssetDTO | str:
        if not os.path.exists(asset_path):
            raise Exception(f'Asset {asset_path} path does not exist')

        if os.path.isdir(asset_path):
            if 'images' in os.path.basename(asset_path):
                return ImageDTO(path=asset_path, is_dir=True)
            elif 'templates' in os.path.basename(asset_path):
                return TemplateDTO(path=asset_path, is_dir=True)
            elif 'printing_objects' in os.path.basename(asset_path):
                return PrintingObjectDTO(path=asset_path, is_dir=True)
            else:
                return asset_path
                # raise Exception(f'Non supported asset type: {asset_path}')
        else:
            if 'images' in os.path.dirname(asset_path):
                return ImageDTO(path=asset_path, is_dir=False)
            elif 'templates' in os.path.dirname(asset_path):
                return TemplateDTO(path=asset_path, is_dir=False)
            elif 'printing_objects' in os.path.dirname(asset_path):
                return PrintingObjectDTO(path=asset_path, is_dir=False)

            else:
                return asset_path
                # raise Exception(f'Non supported asset type: {asset_path}')

    def create_experiment_dir(self, experiment_name: str) -> str:
        experiment_dir_path = os.path.join(self.experiments_home_path, experiment_name)
        os.makedirs(experiment_dir_path, exist_ok=True)
        return experiment_dir_path

    def delete_experiment_dir(self, experiment_name: str):
        experiment_dir_path = os.path.join(self.experiments_home_path, experiment_name)
        if not (os.path.isdir(experiment_dir_path)):
            raise Exception(f'Experiment {experiment_name} does not exist')
        shutil.rmtree(experiment_dir_path)

    def cascade_experiment_renaming(self, experiment_name: str, new_experiment_name: str):
        experiment_dir_path = os.path.join(self.experiments_home_path, experiment_name)
        new_experiment_dir_path = os.path.join(self.experiments_home_path, new_experiment_name)
        if not (os.path.isdir(experiment_dir_path)):
            raise Exception(f'Experiment {experiment_name} does not exist')
        os.rename(experiment_dir_path, new_experiment_dir_path)
        self.rebase_metadata(old_experiment_name=experiment_name,
                             new_experiment_name=new_experiment_name)

    def delete_operation_dir(self, experiment_name: str, operation_id: str):
        operation_dir_path = os.path.join(self.experiments_home_path, experiment_name, operation_id)
        if not (os.path.isdir(operation_dir_path)):
            raise Exception(f'Operation {operation_id} of experiment {experiment_name} does not exist')
        shutil.rmtree(operation_dir_path)

    def prepare_template_to_image_operation_dir(self, experiment_name: str, operation_id: str):
        experiment_dir_path = os.path.join(self.experiments_home_path, experiment_name)
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
        experiment_dir_path = os.path.join(self.experiments_home_path, experiment_name)
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
        experiment_dir_path = os.path.join(self.experiments_home_path, experiment_name)
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

    def prepare_matching_operation_dir(self, experiment_name: str, operation_id: str):
        experiment_dir_path = os.path.join(self.experiments_home_path, experiment_name)
        operation_dir_path = os.path.join(experiment_dir_path, operation_id)
        if os.path.exists(experiment_dir_path) and os.path.isdir(experiment_dir_path):
            os.makedirs(operation_dir_path, exist_ok=True)

            src_templates_set = os.path.join(operation_dir_path, 'src_templates')
            target_templates_set = os.path.join(operation_dir_path, 'target_templates')
            matching_report_csv = os.path.join(operation_dir_path, 'matching_report')
            os.makedirs(src_templates_set, exist_ok=True)
            os.makedirs(target_templates_set, exist_ok=True)
            os.makedirs(matching_report_csv, exist_ok=True)

        else:
            raise Exception(f'Experiment directory {experiment_name} does not exist')

        return operation_dir_path

    def get_sub_templates_dir_path(self, experiment_name: str, operation_id: str) -> str:
        experiment_dir_path = os.path.join(self.experiments_home_path, experiment_name)
        operation_dir_path = os.path.join(experiment_dir_path, operation_id)
        if os.path.exists(experiment_dir_path) and os.path.isdir(experiment_dir_path):
            if os.path.exists(operation_dir_path) and os.path.isdir(operation_dir_path):
                return os.path.join(operation_dir_path, 'templates')
            else:
                raise Exception(f'Operation directory {operation_id} does not exist')
        else:
            raise Exception(f'Experiment directory {experiment_name} does not exist')

    def get_sub_images_dir_path(self, experiment_name: str, operation_id: str) -> str:
        experiment_dir_path = os.path.join(self.experiments_home_path, experiment_name)
        operation_dir_path = os.path.join(experiment_dir_path, operation_id)
        if os.path.exists(experiment_dir_path) and os.path.isdir(experiment_dir_path):
            if os.path.exists(operation_dir_path) and os.path.isdir(operation_dir_path):
                return os.path.join(operation_dir_path, 'images')
            else:
                raise Exception(f'Operation directory {operation_id} does not exist')
        else:
            raise Exception(f'Experiment directory {experiment_name} does not exist')

    def get_sub_min_maps_dir_path(self, experiment_name: str, operation_id: str) -> str:
        experiment_dir_path = os.path.join(self.experiments_home_path, experiment_name)
        operation_dir_path = os.path.join(experiment_dir_path, operation_id)
        if os.path.exists(experiment_dir_path) and os.path.isdir(experiment_dir_path):
            if os.path.exists(operation_dir_path) and os.path.isdir(operation_dir_path):
                return os.path.join(operation_dir_path, 'min_maps')
            else:
                raise Exception(f'Operation directory {operation_id} does not exist')
        else:
            raise Exception(f'Experiment directory {experiment_name} does not exist')

    def get_sub_printing_objects_dir_path(self, experiment_name: str, operation_id: str) -> str:
        experiment_dir_path = os.path.join(self.experiments_home_path, experiment_name)
        operation_dir_path = os.path.join(experiment_dir_path, operation_id)
        if os.path.exists(experiment_dir_path) and os.path.isdir(experiment_dir_path):
            if os.path.exists(operation_dir_path) and os.path.isdir(operation_dir_path):
                return os.path.join(operation_dir_path, 'printing_objects')
            else:
                raise Exception(f'Operation directory {operation_id} does not exist')
        else:
            raise Exception(f'Experiment directory {experiment_name} does not exist')

    def get_sub_src_templates_dir_path(self, experiment_name: str, operation_id: str) -> str:
        experiment_dir_path = os.path.join(self.experiments_home_path, experiment_name)
        operation_dir_path = os.path.join(experiment_dir_path, operation_id)
        if os.path.exists(experiment_dir_path) and os.path.isdir(experiment_dir_path):
            if os.path.exists(operation_dir_path) and os.path.isdir(operation_dir_path):
                return os.path.join(operation_dir_path, 'src_templates')
            else:
                raise Exception(f'Operation directory {operation_id} does not exist')
        else:
            raise Exception(f'Experiment directory {experiment_name} does not exist')

    def get_sub_target_templates_dir_path(self, experiment_name: str, operation_id: str) -> str:
        experiment_dir_path = os.path.join(self.experiments_home_path, experiment_name)
        operation_dir_path = os.path.join(experiment_dir_path, operation_id)
        if os.path.exists(experiment_dir_path) and os.path.isdir(experiment_dir_path):
            if os.path.exists(operation_dir_path) and os.path.isdir(operation_dir_path):
                return os.path.join(operation_dir_path, 'target_templates')
            else:
                raise Exception(f'Operation directory {operation_id} does not exist')
        else:
            raise Exception(f'Experiment directory {experiment_name} does not exist')

    def get_sub_matching_report_csv_path(self, experiment_name: str, operation_id: str) -> str:
        experiment_dir_path = os.path.join(self.experiments_home_path, experiment_name)
        operation_dir_path = os.path.join(experiment_dir_path, operation_id)
        if os.path.exists(experiment_dir_path) and os.path.isdir(experiment_dir_path):
            if os.path.exists(operation_dir_path) and os.path.isdir(operation_dir_path):
                return os.path.join(operation_dir_path, 'matching_report', 'matching_report.csv')
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
        experiment_dir_path = os.path.join(self.experiments_home_path, experiment_name)
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

    def import_src_matching_templates(self, templates_path: str, experiment_name: str, operation_id: str):
        experiment_dir_path = os.path.join(self.experiments_home_path, experiment_name)
        operation_dir_path = os.path.join(experiment_dir_path, operation_id)
        if os.path.exists(experiment_dir_path) and os.path.isdir(experiment_dir_path):
            if os.path.exists(operation_dir_path) and os.path.isdir(operation_dir_path):
                dest_dir_path = self.get_sub_src_templates_dir_path(experiment_name, operation_id)
                shutil.copytree(templates_path, dest_dir_path, dirs_exist_ok=True)
            else:
                raise Exception(f'Operation directory {operation_id} does not exist')
        else:
            raise Exception(f'Experiment directory {experiment_name} does not exist')
        return dest_dir_path

    def import_target_matching_templates(self, templates_path: str, experiment_name: str, operation_id: str):
        experiment_dir_path = os.path.join(self.experiments_home_path, experiment_name)
        operation_dir_path = os.path.join(experiment_dir_path, operation_id)
        if os.path.exists(experiment_dir_path) and os.path.isdir(experiment_dir_path):
            if os.path.exists(operation_dir_path) and os.path.isdir(operation_dir_path):
                dest_dir_path = self.get_sub_target_templates_dir_path(experiment_name, operation_id)
                shutil.copytree(templates_path, dest_dir_path, dirs_exist_ok=True)
            else:
                raise Exception(f'Operation directory {operation_id} does not exist')
        else:
            raise Exception(f'Experiment directory {experiment_name} does not exist')
        return dest_dir_path

    def import_src_matching_template(self, template_path: str, experiment_name: str, operation_id: str) -> str:
        experiment_dir_path = os.path.join(self.experiments_home_path, experiment_name)
        operation_dir_path = os.path.join(experiment_dir_path, operation_id)
        template_name = os.path.basename(template_path)
        if os.path.exists(experiment_dir_path) and os.path.isdir(experiment_dir_path):
            if os.path.exists(operation_dir_path) and os.path.isdir(operation_dir_path):
                dest_dir_path = os.path.join(self.get_sub_src_templates_dir_path(experiment_name, operation_id),
                                             template_name)
                shutil.copy(template_path, dest_dir_path)
            else:
                raise Exception(f'Operation directory {operation_id} does not exist')
        else:
            raise Exception(f'Experiment directory {experiment_name} does not exist')
        return dest_dir_path

    def import_target_matching_template(self, template_path: str, experiment_name: str, operation_id: str) -> str:
        experiment_dir_path = os.path.join(self.experiments_home_path, experiment_name)
        operation_dir_path = os.path.join(experiment_dir_path, operation_id)
        template_name = os.path.basename(template_path)
        if os.path.exists(experiment_dir_path) and os.path.isdir(experiment_dir_path):
            if os.path.exists(operation_dir_path) and os.path.isdir(operation_dir_path):
                dest_dir_path = os.path.join(self.get_sub_target_templates_dir_path(experiment_name, operation_id),
                                             template_name)
                shutil.copy(template_path, dest_dir_path)
            else:
                raise Exception(f'Operation directory {operation_id} does not exist')
        else:
            raise Exception(f'Experiment directory {experiment_name} does not exist')
        return dest_dir_path

    def import_templates_dir(self, templates_path: str, experiment_name: str, operation_id: str) -> str:
        experiment_dir_path = os.path.join(self.experiments_home_path, experiment_name)
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
        experiment_dir_path = os.path.join(self.experiments_home_path, experiment_name)
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
        experiment_dir_path = os.path.join(self.experiments_home_path, experiment_name)
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

    def get_metadata_json_path(self, experiment_name: str, operation_id: str) -> str:
        experiment_dir_path = os.path.join(self.experiments_home_path, experiment_name)
        operation_dir_path = os.path.join(experiment_dir_path, operation_id)
        metadata_json_path = os.path.join(operation_dir_path, 'metadata.json')
        return metadata_json_path

    def register_operation_metadata(self, experiment_name: str, operation: OperationDTO):
        metadata = {
            "operation_id": operation.operation_id,
            "operation_type": operation.operation_type.value,
            "operation_timestamp": operation.operation_datetime.timestamp(),
            "input_asset_path": operation.operation_input.path,
            "optional_extra_asset_path": operation.operation_optional_extra_input.path if not isinstance(operation.operation_optional_extra_input, str) else operation.operation_optional_extra_input,
            "output_asset_path": operation.operation_output.path if not isinstance(operation.operation_output, str) else operation.operation_output
        }
        metadata_path = self.get_metadata_json_path(experiment_name, operation.operation_id)
        with open(metadata_path, 'w') as json_file:
            json.dump(metadata, json_file)

    def rebase_metadata(self, old_experiment_name: str, new_experiment_name: str):
        old_experiment_dir_path = os.path.join(self.experiments_home_path, old_experiment_name)
        new_experiment_dir_path = os.path.join(self.experiments_home_path, new_experiment_name)

        operations_dirs = os.listdir(new_experiment_dir_path)
        for operation_dir in operations_dirs:
            operation_dir_path = os.path.join(new_experiment_dir_path, operation_dir)
            if os.path.isdir(operation_dir_path):
                operation_metadata = self.load_operation_metadata(new_experiment_name, operation_dir)
                input_asset_path = Path(operation_metadata['input_asset_path'])
                output_asset_path = Path(operation_metadata['output_asset_path'])
                input_asset_path = os.path.abspath(os.path.join(new_experiment_dir_path,
                                                                input_asset_path.relative_to(old_experiment_dir_path)))
                output_asset_path = os.path.abspath(os.path.join(new_experiment_dir_path,
                                                                 output_asset_path.relative_to(
                                                                     old_experiment_dir_path)))
                extra_input_asset_path = operation_metadata['optional_extra_asset_path']
                if extra_input_asset_path != '':
                    extra_input_asset_path = os.path.abspath(os.path.join(new_experiment_dir_path,
                                                                     extra_input_asset_path.relative_to(
                                                                         old_experiment_dir_path)))
                operation_metadata['input_asset_path'] = input_asset_path
                operation_metadata['output_asset_path'] = output_asset_path
                operation_metadata['optional_extra_asset_path'] = extra_input_asset_path
                metadata_path = self.get_metadata_json_path(new_experiment_name, operation_dir)
                with open(metadata_path, 'w') as json_file:
                    json.dump(operation_metadata, json_file)

    def load_operation_metadata(self, experiment_name: str, operation_id: str) -> dict:
        metadata_path = self.get_metadata_json_path(experiment_name, operation_id)
        if not os.path.exists(metadata_path):
            raise Exception(f'Operation {operation_id} of experiment {experiment_name} metadata does not exist')
        with open(metadata_path, 'r') as json_file:
            metadata = json.load(json_file)
        return metadata

    def export_data(self, data_path: str, dest_dir_path: str):
        if not os.path.exists(dest_dir_path):
            raise Exception(f'Destination directory {dest_dir_path} does not exist')
        if not os.path.exists(data_path):
            raise Exception(f'Data path {data_path} does not exist')
        if os.path.isdir(data_path):
            shutil.copytree(data_path, os.path.join(dest_dir_path, os.path.basename(data_path)), dirs_exist_ok=False)
        else:
            shutil.copy(src=data_path, dst=os.path.join(dest_dir_path, os.path.basename(data_path)))
