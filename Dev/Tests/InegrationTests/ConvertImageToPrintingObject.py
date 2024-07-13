import os
import os
import unittest

from Dev.DTOs import ImageDTO, PrintingObjectDTO, ExperimentDTO
from Dev.LogicLayer.Service.Service import Service
from TestUtils import images_path


class ConvertImageToPrintingObject(unittest.TestCase):
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

    def test_convert_valid_image_to_printing_object(self):
        valid_image = ImageDTO(
            path=os.path.join(images_path, '109_1_8bit', '109_1_8bit.png'),
            is_dir=False
        )

        response = self.service.convert_image_to_printing_object(valid_image)
        assert response.success
        assert response.data is not None
        generated_printing_object: PrintingObjectDTO = response.data

        assert generated_printing_object.path.endswith('.stl')
        assert os.path.exists(generated_printing_object)

    def test_convert_invalid_image_to_printing_object(self):
        invalid_image = ImageDTO(
            path=os.path.join(images_path, 'bla.png'),
            is_dir=False
        )

        response = self.service.convert_image_to_printing_object(invalid_image)
        assert not response.success
        assert response.data is None

    @classmethod
    def tearDownClass(cls):
        response = cls.service.delete_experiment(cls.experiment_name)
        if not response.success:
            raise response.error


if __name__ == '__main__':
    unittest.main()
