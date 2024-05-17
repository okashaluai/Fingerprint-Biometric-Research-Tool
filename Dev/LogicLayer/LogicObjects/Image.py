from Dev.DTOs import ImageDTO
from Dev.DataAccessLayer.DAOs import ImageDAO
from Dev.LogicLayer.LogicObjects.Asset import Asset
from PIL import Image as PImage
from NBIS.NBIS import detect_minutiae
import os

class Image(Asset):
    def __init__(self, image_path):
        if self.__is_valid_image(image_path):
            super().__init__(image_path)
        else: 
            raise Exception(f'"{image_path}" path does not describe an image location.')

    def to_dto(self) -> ImageDTO:
        raise NotImplementedError

    def to_dao(self) -> ImageDAO:
        raise NotImplementedError

    def __is_valid_image(self, file_path) -> bool:
        try:
            with PImage.open(file_path) as img:
                img.verify()
                return True
        except (IOError, SyntaxError):
            return False
        
    def convert_to_template(self) -> str:
        image_path = str(super().__path)
        template_name = image_path[0:image_path.find(".")]
        detect_minutiae(image_path , Playground.PATH, template_name)
        template_path = os.path.join(Playground.PATH, template_name)
        return template_path


class Playground:
    PATH = ''

    def __init(self):
        raise NotImplementedError
