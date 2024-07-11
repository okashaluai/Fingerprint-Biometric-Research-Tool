import os
from pathlib import Path
import cv2 as cv
import fingerprint_enhancer
from PIL import Image as PImage
from csdt_stl_converter import image2stl
from Dev.DTOs import ImageDTO
from Dev.DataAccessLayer.DAOs import ImageDAO
from Dev.LogicLayer.LogicObjects.Asset import Asset
from Dev.LogicLayer.LogicObjects.PrintingObject import PrintingObject
from Dev.LogicLayer.LogicObjects.Template import Template
from Dev.NBIS.NBIS import detect_minutiae
from Dev.Playground import PLAYGROUND


class Image(Asset):
    def __init__(self, path, is_dir):
        super().__init__(path, is_dir)
        self.__playground = PLAYGROUND()

    def to_dto(self) -> ImageDTO:
        return ImageDTO(path=self.path, is_dir=self.is_dir)

    def to_dao(self) -> ImageDAO:
        raise NotImplementedError

    def __is_valid_image(self, file_path) -> bool:
        try:
            with PImage.open(file_path) as img:
                img.verify()
                return True
        except (IOError, SyntaxError):
            return False

    def convert_to_template(self, experiment_name: str, operation_id: str) -> str:
        image_file_name = os.path.splitext(os.path.basename(self.path))[0]
        self.__playground.prepare_image_to_template_operation_dir(experiment_name, operation_id)
        templates_dir_path = self.__playground.get_sub_templates_dir_path(experiment_name, operation_id)
        images_dir_path = self.__playground.get_sub_images_dir_path(experiment_name, operation_id)
        if self.is_dir:
            self.__playground.import_images_dir(self.path, experiment_name, operation_id)
        else:
            self.__playground.import_image_into_dir(self.path, experiment_name, operation_id)

        detect_minutiae(images_dir_path=images_dir_path, templates_dir_path=templates_dir_path)
        return templates_dir_path

    def convert_to_printing_object(self, experiment_name: str, operation_id: str) -> str:
        self.__playground.prepare_image_to_printing_object_operation_dir(experiment_name, operation_id)
        images_dir_path = self.__playground.get_sub_images_dir_path(experiment_name, operation_id)
        printing_objects_dir_path = self.__playground.get_sub_printing_objects_dir_path(experiment_name, operation_id)
        image_name = os.path.splitext(os.path.basename(self.path))[0]

        if self.is_dir:
            self.__playground.import_images_dir(self.path, experiment_name, operation_id)

        else:
            self.__playground.import_image_into_dir(self.path, experiment_name, operation_id)

        printing_objects_path = build_printing_objects(images_dir_path, printing_objects_dir_path)
        return printing_objects_path


def build_printing_objects(images_dir_path: str, printing_objects_dir_path: str) -> str:
    image_files = os.listdir(images_dir_path)
    printing_objects_path = ''
    for image_file in image_files:
        image_name = os.path.splitext(image_file)[0]
        image_file_path = os.path.join(images_dir_path, image_file)
        image = cv.imread(image_file_path, cv.IMREAD_GRAYSCALE)
        _, binary_image = cv.threshold(image, 128, 255, cv.THRESH_BINARY)
        enhanced_image = fingerprint_enhancer.enhance_Fingerprint(binary_image)
        depth = 0.05

        stl = image2stl.convert_to_stl(255 - enhanced_image, printing_objects_dir_path, base=True,
                                       output_scale=depth)
        printing_objects_path = f'{os.path.join(printing_objects_dir_path, image_name)}.stl'
        with open(printing_objects_path, 'wb') as f:
            f.write(stl)

    if len(image_files) == 1:
        return printing_objects_path
    else:
        return printing_objects_dir_path
