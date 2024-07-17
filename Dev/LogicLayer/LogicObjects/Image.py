import os

import cv2 as cv
import fingerprint_enhancer
from PIL import Image as PImage
from csdt_stl_converter import image2stl

from Dev.DTOs import ImageDTO
from Dev.DataAccessLayer.FILESYSTEM import FILESYSTEM
from Dev.LogicLayer.LogicObjects.Asset import Asset
from Dev.NBIS.NBIS import detect_minutiae


class Image(Asset):
    def __init__(self, path, is_dir):
        super().__init__(path, is_dir)
        self.__filesystem = FILESYSTEM()

    def to_dto(self) -> ImageDTO:
        return ImageDTO(path=self.path, is_dir=self.is_dir)

    def __is_valid_image(self, file_path) -> bool:
        try:
            with PImage.open(file_path) as img:
                img.verify()
                return True
        except (IOError, SyntaxError):
            return False

    def convert_to_template(self, experiment_name: str, operation_id: str) -> str:
        self.__filesystem.prepare_image_to_template_operation_dir(experiment_name, operation_id)
        templates_dir_path = self.__filesystem.get_sub_templates_dir_path(experiment_name, operation_id)
        images_dir_path = self.__filesystem.get_sub_images_dir_path(experiment_name, operation_id)
        if self.is_dir:
            images_path = self.__filesystem.import_images_dir(self.path, experiment_name, operation_id)
            image_names = os.listdir(images_path)
            for image_name in image_names:
                image_path = os.path.join(images_path, image_name)
                self.convert_image_to_png(image_path)
        else:
            image_path = self.__filesystem.import_image_into_dir(self.path, experiment_name, operation_id)
            self.path = self.convert_image_to_png(image_path)

        detect_minutiae(images_dir_path=images_dir_path, templates_dir_path=templates_dir_path)
        return templates_dir_path

    def convert_to_printing_object(self, experiment_name: str, operation_id: str) -> [str, int]:
        self.__filesystem.prepare_image_to_printing_object_operation_dir(experiment_name, operation_id)
        images_dir_path = self.__filesystem.get_sub_images_dir_path(experiment_name, operation_id)
        printing_objects_dir_path = self.__filesystem.get_sub_printing_objects_dir_path(experiment_name, operation_id)

        if self.is_dir:
            images_path = self.__filesystem.import_images_dir(self.path, experiment_name, operation_id)
            image_names = os.listdir(images_path)
            for image_name in image_names:
                image_path = os.path.join(images_path, image_name)
                self.convert_image_to_png(image_path)

        else:
            image_path = self.__filesystem.import_image_into_dir(self.path, experiment_name, operation_id)
            self.path = self.convert_image_to_png(image_path)

        printing_objects_path, converted_successfully_count = build_printing_objects(images_dir_path,
                                                                                     printing_objects_dir_path)
        return printing_objects_path, converted_successfully_count

    def convert_image_to_png(self, image_path: str):
        original_image = PImage.open(image_path)
        image = original_image.copy()
        original_image.close()

        # Convert the image to 8-bit grayscale
        if image.mode != 'L':
            image = image.convert('L')

        # Save the converted image as PNG
        file_name, file_ext = os.path.splitext(image_path)
        output_file = file_name + ".png"
        image.save(output_file, 'PNG')
        image.close()
        if not image_path.endswith('.png'):
            os.remove(image_path)
        return output_file


def build_printing_objects(images_dir_path: str, printing_objects_dir_path: str) -> [str, int]:
    failed_enhancing_image_names = []
    converted_successfully_count = 0

    image_files = os.listdir(images_dir_path)
    printing_objects_path = ''
    for image_file in image_files:
        image_name = os.path.splitext(image_file)[0]
        image_file_path = os.path.join(images_dir_path, image_file)
        image = cv.imread(image_file_path, cv.IMREAD_GRAYSCALE)
        _, binary_image = cv.threshold(image, 128, 255, cv.THRESH_BINARY)

        try:
            enhanced_image = fingerprint_enhancer.enhance_Fingerprint(binary_image)
        except Exception:
            failed_enhancing_image_names.append(image_name)

        if image_name not in failed_enhancing_image_names:
            depth = 0.05

            stl = image2stl.convert_to_stl(255 - enhanced_image, printing_objects_dir_path, base=True,
                                           output_scale=depth)
            printing_objects_path = f'{os.path.join(printing_objects_dir_path, image_name)}.stl'

            with open(printing_objects_path, 'wb') as f:
                f.write(stl)
            converted_successfully_count += 1

    if len(failed_enhancing_image_names) == len(image_files):
        raise Exception("All images failed the enhancing process!")

    if len(image_files) == 1:
        return printing_objects_path, converted_successfully_count
    else:
        return printing_objects_dir_path, converted_successfully_count
