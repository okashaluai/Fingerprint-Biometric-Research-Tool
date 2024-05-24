from Dev.LogicLayer.LogicObjects.Image import Image
from Dev.Utils import Singleton


class ConvertorController(metaclass=Singleton):
    def __init__(self):
        pass

    def convert_image_to_template(self, image_path):
        image = Image(image_path)
        template_path = image.convert_to_template()
        return template_path
