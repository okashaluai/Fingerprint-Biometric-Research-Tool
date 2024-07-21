import datetime
import os.path

from Dev.DTOs import Response, TemplateDTO, ImageDTO
from Dev.LogicLayer.Controllers.ConverterController import ConvertorController
from Dev.LogicLayer.Controllers.ExperimentController import ExperimentController
from Dev.LogicLayer.Controllers.MatcherController import MatcherController
from Dev.LogicLayer.LogicObjects.Asset import Asset
from Dev.LogicLayer.LogicObjects.Image import Image
from Dev.LogicLayer.LogicObjects.Operation import Operation
from Dev.LogicLayer.LogicObjects.Template import Template
from Dev.LogicLayer.Service.IService import IService
from Dev.Utils import Singleton
from Dev.Enums import OperationType
from Dev.DataAccessLayer.FILESYSTEM import FILESYSTEM


class Service(IService, metaclass=Singleton):

    def __init__(self):
        self.__converter_controller = ConvertorController()
        self.__matcher_controller = MatcherController()
        self.__experiment_controller = ExperimentController()
        self.__filesystem: FILESYSTEM = FILESYSTEM()

    def export_asset(self, asset_path: str, export_dest_path: str) -> Response:
        try:
            self.__filesystem.export_data(data_path=asset_path, dest_dir_path=export_dest_path)
            return Response(True, export_dest_path, None)
        except Exception as error:
            return Response(False, None, str(error))

    def convert_template_to_min_map_image(self, template_dto: TemplateDTO) -> Response:
        try:
            template = Template(template_dto.path, template_dto.is_dir)
            min_map_image = self.__converter_controller.convert_template_to_min_map_image(template)
            min_map_image_dto = min_map_image.to_dto()
            return Response(True, min_map_image_dto, None)
        except Exception as error:
            return Response(False, None, str(error))

    def convert_template_to_image(self, template_dto: TemplateDTO) -> Response:
        try:
            current_experiment = self.__experiment_controller.get_current_experiment()

            if template_dto.is_dir:
                operation_type = OperationType.TMPs2IMGs
            else:
                operation_type = OperationType.TMP2IMG

            operation_datetime = datetime.datetime.now()
            operation_id = f'{operation_type.value}_{str(round(operation_datetime.timestamp() * 1000))}'
            template = Template(template_dto.path, template_dto.is_dir)

            image = self.__converter_controller.convert_template_to_image(template,
                                                                          current_experiment.experiment_name,
                                                                          operation_id)
            template.finalize_path(self.__filesystem.get_sub_templates_dir_path(current_experiment.experiment_name,
                                                                                operation_id))
            image.finalize_path()
            operation = Operation(operation_id, operation_type, template, image, operation_datetime)
            self.__experiment_controller.add_operation(operation)
            generated_image = operation.operation_output
            image_dto = generated_image.to_dto()
            return Response(True, image_dto, None)
        except Exception as error:
            self.__experiment_controller.clear_failed_operation(current_experiment.experiment_name, operation_id)
            return Response(False, None, str(error))

    def convert_image_to_template(self, image_dto: ImageDTO) -> Response:
        try:
            current_experiment = self.__experiment_controller.get_current_experiment()

            if image_dto.is_dir:
                operation_type = OperationType.IMGs2TMPs
            else:
                operation_type = OperationType.IMG2TMP
            operation_datetime = datetime.datetime.now()
            operation_id = f'{operation_type.value}_{str(round(operation_datetime.timestamp() * 1000))}'
            image = Image(image_dto.path, image_dto.is_dir)
            template = self.__converter_controller.convert_image_to_template(image,
                                                                             current_experiment.experiment_name,
                                                                             operation_id)
            image.finalize_path(self.__filesystem.get_sub_images_dir_path(current_experiment.experiment_name,
                                                                          operation_id))
            template.finalize_path()
            operation = Operation(operation_id, operation_type, image, template, operation_datetime)
            self.__experiment_controller.add_operation(operation)
            template_dto = template.to_dto()
            return Response(True, template_dto, None)
        except Exception as error:
            self.__experiment_controller.clear_failed_operation(current_experiment.experiment_name, operation_id)
            return Response(False, None, str(error))

    def convert_image_to_printing_object(self, image_dto: ImageDTO) -> Response:
        try:
            current_experiment = self.__experiment_controller.get_current_experiment()

            if image_dto.is_dir:
                operation_type = OperationType.IMGs2POBJs
            else:
                operation_type = OperationType.IMG2POBJ
            operation_datetime = datetime.datetime.now()
            operation_id = f'{operation_type.value}_{str(round(operation_datetime.timestamp() * 1000))}'

            image = Image(image_dto.path, image_dto.is_dir)
            printing_object = self.__converter_controller.convert_image_to_printing_object(image,
                                                                                           current_experiment.experiment_name,
                                                                                           operation_id)
            image.finalize_path(self.__filesystem.get_sub_images_dir_path(current_experiment.experiment_name,
                                                                          operation_id))
            printing_object.finalize_path()
            operation = Operation(operation_id, operation_type, image, printing_object, operation_datetime)
            self.__experiment_controller.add_operation(operation)
            printing_object_dto = printing_object.to_dto()
            return Response(True, printing_object_dto, None)
        except Exception as error:
            self.__experiment_controller.clear_failed_operation(current_experiment.experiment_name, operation_id)
            return Response(False, None, str(error))

    def match_one_to_one(self, src_template_path: str, target_template_path: str) -> Response:
        current_experiment_name = self.__experiment_controller.get_current_experiment().experiment_name
        operation_datetime = datetime.datetime.now()
        operation_id = f'{OperationType.OneVsOneMatching.value}_{str(round(operation_datetime.timestamp() * 1000))}'

        try:
            self.__filesystem.prepare_matching_operation_dir(experiment_name=current_experiment_name,
                                                           operation_id=operation_id)
            local_src_template_path = self.__filesystem.import_src_matching_template(experiment_name=current_experiment_name,
                                                                                     operation_id=operation_id,
                                                                                     template_path=src_template_path)
            local_target_template_path = self.__filesystem.import_target_matching_template(experiment_name=current_experiment_name,
                                                                                           operation_id=operation_id,
                                                                                           template_path=target_template_path)

            matching_score = self.__matcher_controller.match_one_to_one(local_src_template_path, local_target_template_path)

            csv_path = self.__filesystem.get_sub_matching_report_csv_path(experiment_name=current_experiment_name,
                                                                           operation_id=operation_id)
            self.__matcher_controller.write_one_to_one_score_as_csv(local_src_template_path,
                                                                    local_target_template_path,
                                                                    matching_score,
                                                                    csv_path)

            operation = Operation(operation_id=operation_id,
                                  operation_type=OperationType.OneVsOneMatching,
                                  operation_input= Template(local_src_template_path, is_dir=False),
                                  operation_datetime=operation_datetime,
                                  operation_optional_extra_input=Template(local_target_template_path, is_dir=False),
                                  operation_output=csv_path)
            self.__experiment_controller.add_operation(operation)

            return Response(True, matching_score, None)
        except Exception as error:
            self.__experiment_controller.clear_failed_operation(current_experiment_name, operation_id)
            return Response(False, None, str(error))

    def match_one_to_many(self, src_template_path: str, target_templates_dir_path: str) -> Response:
        try:
            current_experiment_name = self.__experiment_controller.get_current_experiment().experiment_name
            operation_datetime = datetime.datetime.now()
            operation_id = f'{OperationType.OneVsManyMatching.value}_{str(round(operation_datetime.timestamp() * 1000))}'

            self.__filesystem.prepare_matching_operation_dir(experiment_name=current_experiment_name,
                                                             operation_id=operation_id)
            local_src_template_path = self.__filesystem.import_src_matching_template(
                experiment_name=current_experiment_name,
                operation_id=operation_id,
                template_path=src_template_path)
            local_target_templates_dir_path = self.__filesystem.import_target_matching_templates(
                experiment_name=current_experiment_name,
                operation_id=operation_id,
                templates_path=target_templates_dir_path)

            matching_score = self.__matcher_controller.match_one_to_many(local_src_template_path,
                                                                        local_target_templates_dir_path)

            csv_path = self.__filesystem.get_sub_matching_report_csv_path(experiment_name=current_experiment_name,
                                                                          operation_id=operation_id)
            self.__matcher_controller.write_matrix_score_as_csv(matching_score,
                                                                csv_path)

            operation = Operation(operation_id=operation_id,
                                  operation_type=OperationType.OneVsManyMatching,
                                  operation_input=Template(local_src_template_path, is_dir=False),
                                  operation_datetime=operation_datetime,
                                  operation_optional_extra_input=Template(local_target_templates_dir_path, is_dir=True),
                                  operation_output=csv_path)
            self.__experiment_controller.add_operation(operation)

            return Response(True, matching_score, None)
        except Exception as error:
            self.__experiment_controller.clear_failed_operation(current_experiment_name, operation_id)
            return Response(False, None, str(error))

    def match_many_to_many(self, src_templates_dir_path: str, target_templates_dir_path: str) -> Response:
        try:
            current_experiment_name = self.__experiment_controller.get_current_experiment().experiment_name
            operation_datetime = datetime.datetime.now()
            operation_id = f'{OperationType.ManyVsManyMatching.value}_{str(round(operation_datetime.timestamp() * 1000))}'

            self.__filesystem.prepare_matching_operation_dir(experiment_name=current_experiment_name,
                                                             operation_id=operation_id)
            local_src_templates_dir_path = self.__filesystem.import_src_matching_templates(
                experiment_name=current_experiment_name,
                operation_id=operation_id,
                templates_path=src_templates_dir_path)
            local_target_templates_dir_path = self.__filesystem.import_target_matching_templates(
                experiment_name=current_experiment_name,
                operation_id=operation_id,
                templates_path=target_templates_dir_path)

            matching_score = self.__matcher_controller.match_many_to_many(local_src_templates_dir_path,
                                                                        local_target_templates_dir_path)

            csv_path = self.__filesystem.get_sub_matching_report_csv_path(experiment_name=current_experiment_name,
                                                                          operation_id=operation_id)
            self.__matcher_controller.write_matrix_score_as_csv(matching_score,
                                                                csv_path)

            operation = Operation(operation_id=operation_id,
                                  operation_type=OperationType.ManyVsManyMatching,
                                  operation_input=Template(local_src_templates_dir_path, is_dir=True),
                                  operation_datetime=operation_datetime,
                                  operation_optional_extra_input=Template(local_target_templates_dir_path, is_dir=True),
                                  operation_output=csv_path)
            self.__experiment_controller.add_operation(operation)

            return Response(True, matching_score, None)
        except Exception as error:
            self.__experiment_controller.clear_failed_operation(current_experiment_name, operation_id)
            return Response(False, None, str(error))

    def export_matching_matrix_csv(self, score_matrix, export_full_path: str) -> Response:
        try:
            self.__matcher_controller.write_matrix_score_as_csv(score_matrix, export_full_path)
            return Response(True, None, None)
        except Exception as error:
            return Response(False, None, str(error))

    def export_matching_one_to_one_csv(self, template1_path, template2_path, score,
                                       export_full_path: str) -> Response:
        try:
            self.__matcher_controller.write_one_to_one_score_as_csv(template1_path, template2_path, score,
                                                                    export_full_path)
            return Response(True, None, None)
        except Exception as error:
            return Response(False, None, str(error))

    def get_experiments(self) -> Response:
        try:
            experiments = self.__experiment_controller.get_experiments()
            experiments_dtos = list()
            for experiment in experiments:
                experiment_dto = experiment.to_dto()
                experiments_dtos.append(experiment_dto)
            return Response(True, experiments_dtos, None)
        except Exception as error:
            return Response(False, None, str(error))

    def delete_experiment(self, experiment_name: str) -> Response:
        try:
            self.__experiment_controller.delete_experiment(experiment_name)
            return Response(True, None, None)
        except Exception as error:
            return Response(False, None, str(error))

    def export_experiment(self, experiment_name: str, export_path: str) -> Response:
        try:
            self.__experiment_controller.export_experiment(experiment_name, export_path)
            return Response(True, export_path, None)
        except Exception as error:
            return Response(False, None, str(error))

    def rename_experiment(self, experiment_name: str, new_experiment_name: str) -> Response:
        try:
            updated_experiment = self.__experiment_controller.rename_experiment(experiment_name, new_experiment_name)
            updated_experiment_dto = updated_experiment.to_dto()
            return Response(True, updated_experiment_dto, None)
        except Exception as error:
            return Response(False, None, str(error))

    def create_experiment(self, experiment_name: str) -> Response:
        try:
            new_experiment = self.__experiment_controller.create_experiment(experiment_name)
            new_experiment_dto = new_experiment.to_dto()
            return Response(True, new_experiment_dto, None)
        except Exception as error:
            return Response(False, None, str(error))

    def set_current_experiment(self, experiment_name: str) -> Response:
        try:
            current_experiment = self.__experiment_controller.set_current_experiment(experiment_name)
            current_experiment_dto = current_experiment.to_dto()
            return Response(True, current_experiment_dto, None)
        except Exception as error:
            return Response(False, None, str(error))

    def get_current_experiment(self) -> Response:
        try:
            current_experiment = self.__experiment_controller.get_current_experiment()
            current_experiment_dto = current_experiment.to_dto()
            return Response(True, current_experiment_dto, None)
        except Exception as error:
            return Response(False, None, str(error))

    def delete_operation(self, experiment_name: str, operation_id: str) -> Response:
        try:
            self.__experiment_controller.delete_operation(experiment_name, operation_id)
            return Response(True, None, None)
        except Exception as error:
            return Response(False, None, str(error))

# service = Service()
# service.rename_experiment('exp2', 'exp9')
# service.create_experiment('test1')
# service.set_current_experiment('test1')
# t1 = TemplateDTO('', is_dir=False)
# t2 = TemplateDTO('', is_dir=True)
# img1 = ImageDTO('/home/z01x/Desktop/Images/1.png', is_dir=False)
# img2 = ImageDTO('/home/z01x/Desktop/Images', is_dir=True)
# t1 = service.convert_image_to_template(img1)
# t2 = service.convert_image_to_template(img2)
# po1 = service.convert_image_to_printing_object(img1)
# po2 = service.convert_image_to_printing_object(img2)
# path = os.path.join(t1.path, os.path.splitext(os.path.basename(img1.path))[0] + '.min')
# t = TemplateDTO(path, is_dir=False)
# service.convert_template_to_image(t)
# service.convert_template_to_image(t2)
# service.rename_experiment('test1', 'renamed_test')
# r1 = service.match_many_to_many('/home/z01x/Desktop/Fingerprint Biometric Research Tool/Final_Project/Dev/Tests/Assets/Templates/many_templates', '/home/z01x/Desktop/Fingerprint Biometric Research Tool/Final_Project/Dev/Tests/Assets/Templates/many_templates')
# r2 = service.match_one_to_many('/home/z01x/Desktop/Fingerprint Biometric Research Tool/Final_Project/Dev/Tests/Assets/Templates/109_3_8bit/109_3_8bit.xyt', '/home/z01x/Desktop/Fingerprint Biometric Research Tool/Final_Project/Dev/Tests/Assets/Templates/many_templates')
# r3 = service.match_one_to_one('/home/z01x/Desktop/Fingerprint Biometric Research Tool/Final_Project/Dev/Tests/Assets/Templates/109_3_8bit/109_3_8bit.xyt', '/home/z01x/Desktop/Fingerprint Biometric Research Tool/Final_Project/Dev/Tests/Assets/Templates/109_3_8bit/109_3_8bit.xyt')
# exps = service.get_experiments().data
# print('DONE')
