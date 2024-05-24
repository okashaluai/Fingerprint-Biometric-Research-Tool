import os
from pathlib import Path

from PIL import Image as PImage

from Dev.DTOs import ImageDTO
from Dev.DataAccessLayer.DAOs import ImageDAO
from Dev.LogicLayer.LogicObjects.Asset import Asset
from Dev.NBIS.NBIS import detect_minutiae
from Dev.Playground import PLAYGROUND


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
        image_path = str(self.__path)
        template_name = Path(image_path).stem
        detect_minutiae(image_path, PLAYGROUND.PATH, template_name)
        template_path = os.path.join(PLAYGROUND.PATH, template_name)
        return template_path



# For Testing
# from Dev.FingerprintGenerator.generator import generate
# generate(r'/home/z01x/Desktop/Fingerprint Biometric Research Tool/Final_Project/Dev/FingerprintGenerator/temp', r'/home/z01x/Desktop/Fingerprint Biometric Research Tool/Final_Project/Dev/FingerprintGenerator/temp')