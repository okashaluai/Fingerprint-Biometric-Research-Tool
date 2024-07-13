import datetime
from Dev.DTOs import Response, TemplateDTO, ImageDTO
from Dev.LogicLayer.Controllers.ConverterController import ConvertorController
from Dev.LogicLayer.Controllers.ExperimentController import ExperimentController
from Dev.LogicLayer.Controllers.MatcherController import MatcherController
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
            return Response(False, None, str(error))

    def match_one_to_one(self, template1_path: str, template2_path: str) -> Response:
        try:
            score = self.__matcher_controller.match_one_to_one(template1_path, template2_path)
            return Response(True, score, None)
        except Exception as error:
            return Response(False, None, str(error))

    def match_one_to_many(self, template_path: str, templates_dir_path: str) -> Response:
        try:
            score = self.__matcher_controller.match_one_to_many(template_path, templates_dir_path)
            return Response(True, score, None)
        except Exception as error:
            return Response(False, None, str(error))

    def match_many_to_many(self, templates1_dir_path: str, templates2_dir_path: str) -> Response:
        try:
            score = self.__matcher_controller.match_many_to_many(templates1_dir_path, templates2_dir_path)
            return Response(True, score, None)
        except Exception as error:
            return Response(False, None, str(error))

    def export_matching_matrix_csv(self, score_matrix, export_full_path: str) -> Response:
        try:
            self.__matcher_controller.export_matrix_score_as_csv(score_matrix, export_full_path)
            return Response(True, None, None)
        except Exception as error:
            return Response(False, None, str(error))

    def export_matching_one_to_one_csv(self, template1_path, template2_path, score,
                                       export_full_path: str) -> Response:
        try:
            self.__matcher_controller.export_one_to_one_score_as_csv(template1_path, template2_path, score,
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


service = Service()
# service.delete_experiment('exp2')
e = service.create_experiment('exp2')
service.set_current_experiment('exp2')
exps = service.get_experiments()
img1 = ImageDTO(r'C:\Users\Yazan\Desktop\Final_Project\Dev\Tests\Assets\Images\109_1_8bit\109_1_8bit.png', is_dir=False)
# img2 = ImageDTO('/home/z01x/Desktop/Images', is_dir=True)
t1 = service.convert_image_to_printing_object(img1)
# t2 = service.convert_image_to_printing_object(img2)
# cr = service.get_current_experiment()
print('DONE')
