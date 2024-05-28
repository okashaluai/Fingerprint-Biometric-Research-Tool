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

    def convert_template_to_image(self, experiment_name: str, template_dto: TemplateDTO) -> Response:
        try:
            image = self.__converter_controller.convert_template_to_image(experiment_name, template_dto.path)
            image_dto = image.to_dto()
            return Response(True, image_dto, None)
        except Exception as error:
            return Response(False, None, str(error))

    def convert_image_to_template(self, experiment_name: str, image_dto: ImageDTO) -> Response:
        try:
            template = self.__converter_controller.convert_image_to_template(experiment_name, image_dto.path)
            template_dto = template.to_dto()
            return Response(True, template_dto, None)
        except Exception as error:
            return Response(False, None, str(error))

    def convert_image_to_printing_object(self, experiment_name: str, image_dto: ImageDTO) -> Response:
        try:
            printing_object = self.__converter_controller.convert_image_to_printing_object(experiment_name,
                                                                                           image_dto.path)
            printing_object_dto = printing_object.to_dto()
            return Response(True, printing_object_dto, None)
        except Exception as error:
            return Response(False, None, str(error))

    def match(self, experiment_name: str, templates_path1: tuple[str], templates_path2: tuple[str]) -> Response:
        try:
            score = self.__matcher_controller.match_templates(templates_path1, templates_path2)
            return Response(True, score, None)
        except Exception as error:
            return Response(False, None, str(error))

    def get_experiments(self) -> Response:
        try:
            raise NotImplementedError
        except Exception as error:
            return Response(False, None, str(error))

    def delete_experiment(self, experiment_name: str) -> Response:
        try:
            raise NotImplementedError
        except Exception as error:
            return Response(False, None, str(error))

    def export_experiment(self, experiment_name: str) -> Response:
        try:
            raise NotImplementedError
        except Exception as error:
            return Response(False, None, str(error))

    def rename_experiment(self, experiment_name: str, new_name: str) -> Response:
        try:
            raise NotImplementedError
        except Exception as error:
            return Response(False, None, str(error))

    def create_experiment(self, experiment_name: str) -> Response:
        try:
            raise NotImplementedError
        except Exception as error:
            return Response(False, None, str(error))

    def set_current_experiment(self, experiment_name: str) -> Response:
        try:
            raise NotImplementedError
        except Exception as error:
            return Response(False, None, str(error))
