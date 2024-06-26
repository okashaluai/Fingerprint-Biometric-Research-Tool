from Dev.DTOs import Response, TemplateDTO, ImageDTO
from Dev.LogicLayer.Controllers.ConverterController import ConvertorController
from Dev.LogicLayer.Controllers.ExperimentController import ExperimentController
from Dev.LogicLayer.Controllers.MatcherController import MatcherController
from Dev.LogicLayer.Service.IService import IService
from Dev.Utils import Singleton


class Service(IService, metaclass=Singleton):
    def __init__(self):
        self.__converter_controller = ConvertorController()
        self.__matcher_controller = MatcherController()
        self.__experiment_controller = ExperimentController()

    def convert_template_to_image(self, template_dto: TemplateDTO) -> Response:
        try:
            image = self.__converter_controller.convert_template_to_image(template_dto.path)
            image_dto = image.to_dto()
            return Response(True, image_dto, None)
        except Exception as error:
            return Response(False, None, str(error))

    def convert_image_to_template(self, image_dto: ImageDTO) -> Response:
        try:
            template = self.__converter_controller.convert_image_to_template(image_dto.path)
            template_dto = template.to_dto()
            return Response(True, template_dto, None)
        except Exception as error:
            return Response(False, None, str(error))

    def convert_image_to_printing_object(self, image_dto: ImageDTO) -> Response:
        try:
            printing_object = self.__converter_controller.convert_image_to_printing_object(image_dto.path)
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
            experiments = self.__experiment_controller.get_sorted_experiments_by_date()
            experiments_dtos = list()
            for experiment in experiments:
                experiment_dto = experiment.to_dto()
                experiments_dtos.append(experiment_dto)
            return Response(True, experiments_dtos, None)
        except Exception as error:
            return Response(False, None, str(error))

    def delete_experiment(self, experiment_id: int) -> Response:
        try:
            self.__experiment_controller.delete_experiment(experiment_id)
            return Response(True, None, None)
        except Exception as error:
            return Response(False, None, str(error))

    def export_experiment(self, experiment_id: int, export_path: str) -> Response:
        try:
            self.__experiment_controller.export_experiment(experiment_id, export_path)
            return Response(True, export_path, None)
        except Exception as error:
            return Response(False, None, str(error))

    def rename_experiment(self, experiment_id: int, new_experiment_name: str) -> Response:
        try:
            updated_experiment = self.__experiment_controller.rename_experiment(experiment_id, new_experiment_name)
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

    def set_current_experiment(self, experiment_id: int) -> Response:
        try:
            current_experiment = self.__experiment_controller.set_current_experiment(experiment_id)
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

    def delete_operation(self, experiment_id: int, operation_id: int) -> Response:
        try:
            self.__experiment_controller.delete_operation(experiment_id, operation_id)
            return Response(True, None, None)
        except Exception as error:
            return Response(False, None, str(error))
