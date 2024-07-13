import os
import unittest
from pathlib import Path

from Dev.DTOs import ImageDTO, TemplateDTO, ExperimentDTO
from Dev.LogicLayer.Service.Service import Service
from TestUtils import images_path, templates_path


class MinMapCreation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.service = Service()

    @unittest.skip
    def test_convert_valid_template_to_image(self):
        valid_template = TemplateDTO(
            path=os.path.join(templates_path, '109_1_8bit', '109_1_8bit.min'),
            is_dir=False
        )

        response = self.service.convert_template_to_min_map_image(valid_template)
        assert response.success
        assert response.data is not None
        generated_image: ImageDTO = response.data

        assert os.path.exists(generated_image.path)
        assert generated_image.path.endswith('109_1_8bit.png')

    @unittest.skip
    def test_convert_many_templates_to_many_images(self):
        valid_template = TemplateDTO(
            path=os.path.join(templates_path, 'many_templates_for_convert'),
            is_dir=True
        )

        response = self.service.convert_template_to_min_map_image(valid_template)
        assert response.success
        assert response.data is not None
        generated_image: ImageDTO = response.data

        assert generated_image.path != ""
        assert os.path.exists(generated_image.path)

        files_counter = 0
        for t in os.listdir(valid_template.path):
            base_name = Path(t).stem
            for im in os.listdir(generated_image.path):
                if im.startswith(base_name):
                    files_counter += 1

        assert files_counter == len(os.listdir(valid_template.path))

    def test_invalid_template_to_min_map(self):
        invalid_template = TemplateDTO(
            path=os.path.join(templates_path, 'bla.min'),
            is_dir=False
        )

        response = self.service.convert_template_to_min_map_image(invalid_template)
        assert not response.success
        assert response.data is None


if __name__ == '__main__':
    unittest.main()
