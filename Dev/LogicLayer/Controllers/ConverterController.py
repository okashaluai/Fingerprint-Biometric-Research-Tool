from Dev.Enums import OperationType
from Dev.LogicLayer.Controllers.ExperimentController import ExperimentController
from Dev.LogicLayer.LogicObjects.Image import Image
from Dev.LogicLayer.LogicObjects.PrintingObject import PrintingObject
from Dev.LogicLayer.LogicObjects.Template import Template
from Dev.Utils import Singleton


class ConvertorController(metaclass=Singleton):

    def __init__(self):
        self.__experiment_controller = ExperimentController()

    def convert_template_to_image(self, template_path: str) -> Image:
        template = Template(template_path)
        image = template.convert_to_image()

        # Add this operation to the current experiment
        new_operation = self.__experiment_controller.add_operation(OperationType.TMP2IMG, template.path, image.path)

        return image

    def convert_image_to_template(self, image_path: str) -> Template:
        image = Image(image_path)
        template = image.convert_to_template()

        # Add this operation to the current experiment
        new_operation = self.__experiment_controller.add_operation(OperationType.IMG2TMP, image.path, template.path)

        return template

    def convert_image_to_printing_object(self, image_path: str) -> PrintingObject:
        image = Image(image_path)
        printing_object = image.convert_to_printing_object()

        # Add this operation to the current experiment
        new_operation = self.__experiment_controller.add_operation(OperationType.IMG2POBJ, image.path,
                                                                   printing_object.path)

        return printing_object
