from Dev.LogicLayer.LogicObjects.Image import Image
from Dev.LogicLayer.LogicObjects.PrintingObject import PrintingObject
from Dev.LogicLayer.LogicObjects.Template import Template
from Dev.Utils import Singleton
from Dev.DataAccessLayer.FILESYSTEM import FILESYSTEM


class ConvertorController(metaclass=Singleton):

    def __init__(self):
        self.__filesystem = FILESYSTEM()
        self.__min_maps_cache: dict[str, str] = dict()

    def convert_template_to_min_map_image(self, template: Template):
        min_map_image_path = ''
        if template.path in self.__min_maps_cache:
            min_map_image_path = self.__min_maps_cache.get(template.path)
        else:
            min_map_image_path = template.convert_to_min_map_image()
            self.__min_maps_cache[template.path] = min_map_image_path
        min_map_image = Image(min_map_image_path, is_dir=False)
        return min_map_image

    def convert_template_to_image(self, template: Template, experiment_name: str, operation_id: str) -> Image:
        generated_image_path = template.convert_to_image(experiment_name, operation_id)
        generated_image = Image(generated_image_path, template.is_dir)
        return generated_image

    def convert_image_to_template(self, image: Image, experiment_name: str, operation_id: str) -> Template:
        template_path = image.convert_to_template(experiment_name, operation_id)
        extracted_template = Template(template_path, image.is_dir)
        return extracted_template

    def convert_image_to_printing_object(self, image: Image, experiment_name: str, operation_id: str) -> PrintingObject:
        printing_object_path, converted_successfully_count = image.convert_to_printing_object(experiment_name, operation_id)
        built_printing_object = PrintingObject(printing_object_path, image.is_dir, converted_successfully_count)
        return built_printing_object
