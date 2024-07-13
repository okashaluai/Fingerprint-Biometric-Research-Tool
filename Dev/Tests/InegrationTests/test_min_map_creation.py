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

    def test_single_min_map_creation(self):
        valid_template = TemplateDTO(
            path=os.path.join(templates_path, '109_1_8bit', '109_1_8bit.min'),
            is_dir=False
        )
        os.path.exists(valid_template.path)
        response = self.service.convert_template_to_min_map_image(valid_template)
        assert response.success
        assert response.data is not None

        generated_image: ImageDTO = response.data

        assert os.path.exists(generated_image.path)
        assert generated_image.path.endswith('109_1_8bit.png')

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
