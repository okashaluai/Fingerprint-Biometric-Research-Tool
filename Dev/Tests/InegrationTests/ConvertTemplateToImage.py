import datetime
import os
import unittest

from Dev.DTOs import ImageDTO, TemplateDTO
from Dev.LogicLayer.Service.Service import Service
from TestUtils import images_path, templates_path


class ConvertTemplateToImage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.service = Service()
        # Create experiment
        cls.experiment_name = "IT_Experiment"
        create_experiment_response = cls.service.create_experiment(cls.experiment_name)
        if create_experiment_response.success:
            pass
        else:
            raise create_experiment_response.error

        # Set current experiment
        set_current_experiment_response = cls.service.set_current_experiment(cls.experiment_name)
        if set_current_experiment_response.success:
            pass
        else:
            raise set_current_experiment_response.error

    def test_convert_valid_template_to_image(self):
        valid_template = TemplateDTO(
            path=os.path.join(templates_path, '109_1_8bit_template', '109_1_8bit_template.min'),
            date=datetime.datetime.now(),
            is_dir=False
        )

        response = self.service.convert_template_to_image(valid_template)
        assert response.success
        assert response.data is not None
        generated_image: ImageDTO = response.data

        # assert generated_image.path.endswith('109_1_8bit_template.png')

        # assert os.path.exists(generated_image.path)

    def test_convert_invalid_template_to_image(self):
        invalid_template = TemplateDTO(
            path=os.path.join(images_path, 'bla.png'),
            date=datetime.datetime.now(),
            is_dir=False
        )

        response = self.service.convert_template_to_image(invalid_template)
        assert not response.success
        assert response.data is None

    @classmethod
    def tearDownClass(cls):
        response = cls.service.delete_experiment(cls.experiment_name)
        if not response.success:
            raise response.error


if __name__ == '__main__':
    unittest.main()
