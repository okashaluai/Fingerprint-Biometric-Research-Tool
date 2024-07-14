import os.path
from Dev.DTOs import TemplateDTO
from Dev.LogicLayer.LogicObjects.Asset import Asset
from Dev.FingerprintGenerator.generator import generate_image, generate_images, create_temp_minutiae_map_image
from Dev.DataAccessLayer.FILESYSTEM import FILESYSTEM


class Template(Asset):
    def __init__(self, path, is_dir):
        super().__init__(path, is_dir)
        self.__filesystem = FILESYSTEM()

    def convert_to_image(self, experiment_name: str, operation_id: str) -> str:
        template_file_name = os.path.splitext(os.path.basename(self.path))[0]
        self.__filesystem.prepare_template_to_image_operation_dir(experiment_name, operation_id)
        templates_dir_path = self.__filesystem.get_sub_templates_dir_path(experiment_name, operation_id)
        min_map_dir_path = self.__filesystem.get_sub_min_maps_dir_path(experiment_name, operation_id)
        image_dir_path = self.__filesystem.get_sub_images_dir_path(experiment_name, operation_id)
        image_path = ''
        if self.is_dir:
            self.__filesystem.import_templates_dir(self.path, experiment_name, operation_id)
            generate_images(templates_dir_path, min_map_dir_path, image_dir_path)
            image_path = image_dir_path
        else:
            self.__filesystem.import_template_into_dir(self.path, experiment_name, operation_id)
            generate_image(templates_dir_path, min_map_dir_path, image_dir_path)
            image_path = os.path.join(image_dir_path, template_file_name + '_fake.png')
        return image_path

    def to_dto(self) -> TemplateDTO:
        return TemplateDTO(path=self.path, is_dir=self.is_dir)

    def __eq__(self, other):
        f1_min_content = []
        f1_xyt_content = []
        f2_min_content = []
        f2_xyt_content = []

        with open(self.path.join('.min')) as f:
            f1_min_content = f.readlines()

        with open(self.path.join('.xyt')) as f:
            f1_xyt_content = f.readlines()

        with open(other.path.join('.min')) as f:
            f2_min_content = f.readlines()

        with open(other.path.join('.xyt')) as f:
            f2_xyt_content = f.readlines()

        return (f1_min_content.sort() == f2_min_content.sort()) and (f1_xyt_content.sort() == f2_xyt_content.sort())

    def convert_to_min_map_image(self):
        template_path = self.__filesystem.import_temp_template(self.path)
        min_map_dir_path = self.__filesystem.get_temp_min_maps_dir_path()
        min_map_image_path = create_temp_minutiae_map_image(template_path, min_map_dir_path)
        return min_map_image_path
