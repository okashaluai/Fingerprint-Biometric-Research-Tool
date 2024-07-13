import os
import unittest
from pathlib import Path

from Dev.DTOs import ImageDTO, TemplateDTO, ExperimentDTO
from Dev.LogicLayer.Service.Service import Service
from TestUtils import images_path, templates_path


class ConvertTemplateToImage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.service = Service()
        cls.experiment_name = "IT_Experiment"

        # Clean dangling experiment
        get_all_experiments_response = cls.service.get_experiments()
        if not get_all_experiments_response.success:
            raise get_all_experiments_response.error
        experiments: list[ExperimentDTO] = get_all_experiments_response.data

        for e in experiments:
            if e.experiment_name == cls.experiment_name:
                response = cls.service.delete_experiment(cls.experiment_name)
                if not response.success:
                    raise response.error

        # Create experiment
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
            path=os.path.join(templates_path, '109_1_8bit', '109_1_8bit.min'),
            is_dir=False
        )

        response = self.service.convert_template_to_image(valid_template)
        assert response.success
        assert response.data is not None
        generated_image: ImageDTO = response.data

        assert os.path.exists(generated_image.path)
        assert generated_image.path.endswith('109_1_8bit.png')

    def test_convert_many_templates_to_many_images(self):
        valid_template = TemplateDTO(
            path=os.path.join(templates_path, 'many_templates_for_convert'),
            is_dir=True
        )

        response = self.service.convert_template_to_image(valid_template)
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

        assert files_counter >= len(os.listdir(valid_template.path))

    def test_convert_invalid_template_to_image(self):
        invalid_template = TemplateDTO(
            path=os.path.join(images_path, 'bla.png'),

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
