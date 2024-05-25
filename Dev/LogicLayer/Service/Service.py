import time

from Dev.DTOs import OperationDTO, Response, TemplateDTO, ImageDTO
from Dev.LogicLayer.Controllers.ConverterController import ConvertorController
from Dev.LogicLayer.Controllers.ExperimentController import ExperimentController
from Dev.LogicLayer.Controllers.MatcherController import MatcherController
from Dev.LogicLayer.Service.IService import IService


class Service(IService):

    def __init__(self):
        self.convertor_controller = ConvertorController()
        self.experiment_controller = ExperimentController()
        self.convertor_controller = MatcherController()

    def convert_template_to_image(self, experiment_name: str, template_dto: TemplateDTO) -> Response:
        try:
            raise NotImplementedError
        except Exception as error:
            return Response(False, None, str(error))

    def convert_image_to_template(self, experiment_name: str, image_dto: ImageDTO) -> Response:
        try:
            template = ConvertorController().convert_image_to_template(experiment_name, image_dto.path)
            template_dto = template.to_dto()
            return Response(True, template_dto, None)
        except Exception as error:
            return Response(False, None, str(error))

    def convert_image_to_printing_object(self, experiment_name: str, image_dto: ImageDTO) -> Response:
        try:
            printing_object = ConvertorController().convert_image_to_printing_object(experiment_name, image_dto.path)
            printing_object_dto = printing_object.to_dto()
            return Response(True, printing_object_dto, None)
        except Exception as error:
            return Response(False, None, str(error))

    def match(self, templates_path1: tuple[str], templates_path2: tuple[str]) -> Response:
        try:
            raise NotImplementedError
        except Exception as error:
            return Response(False, None, str(error))

    def get_experiments(self) -> Response:
        try:
            raise NotImplementedError
        except Exception as error:
            return Response(False, None, str(error))

    def delete_experiment(self, experiment_id: int) -> Response:
        try:
            raise NotImplementedError
        except Exception as error:
            return Response(False, None, str(error))

    def export_experiment(self, experiment_id: int) -> Response:
        try:
            raise NotImplementedError
        except Exception as error:
            return Response(False, None, str(error))

    def rename_experiment(self, experiment_id: int, name: str) -> Response:
        try:
            raise NotImplementedError
        except Exception as error:
            return Response(False, None, str(error))

    def create_experiment(self, name: str) -> Response:
        try:
            raise NotImplementedError
        except Exception as error:
            return Response(False, None, str(error))

    def add_operation(self, experiment_id: int, operation: OperationDTO) -> Response:
        try:
            raise NotImplementedError
        except Exception as error:
            return Response(False, None, str(error))


# response = Service().convert_image_to_printing_object("yazan experiment",
#                                                       r"C:\Users\Yazan\Desktop\3526_2_real_fake.png")

response = Service().convert_image_to_template("exp",
                                               ImageDTO(id=0, date=time.time(),
                                                        path=r"C:\Users\Yazan\Desktop\Final_Project\Dev\Tests\Assets\Image2Template\TestCase1\i1.png"))
print(response.success)
print(response.error)
print(response.data.path)
