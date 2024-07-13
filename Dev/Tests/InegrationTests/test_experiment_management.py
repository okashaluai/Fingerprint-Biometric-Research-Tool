import os
import unittest

from Dev.DTOs import ImageDTO, TemplateDTO, ExperimentDTO
from Dev.Enums import OperationType
from Dev.LogicLayer.Service.Service import Service
from TestUtils import images_path


class ExperimentManagement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.service = Service()
        cls.experiment_names = ["NewExperiment",
                                "OldName",
                                "NewName",
                                "ConvertExperiment",
                                "OldExperiment"]

        # Clean dangling experiment
        get_all_experiments_response = cls.service.get_experiments()
        if not get_all_experiments_response.success:
            raise get_all_experiments_response.error
        experiments: list[ExperimentDTO] = get_all_experiments_response.data

        for e in experiments:
            if e.experiment_name in cls.experiment_names:
                response = cls.service.delete_experiment(e.experiment_name)
                if not response.success:
                    raise response.error

    def test_create_delete_experiment(self):
        experiment_name = "NewExperiment"
        create_experiment_response = self.service.create_experiment(experiment_name)
        if not create_experiment_response.success:
            raise create_experiment_response.error

        experiment_dto: ExperimentDTO = create_experiment_response.data

        assert experiment_dto.experiment_name == experiment_name

        delete_experiment_response = self.service.delete_experiment(experiment_name)
        if not delete_experiment_response.success:
            raise delete_experiment_response.error

    def test_rename_experiment(self):
        experiment_name = "OldName"
        new_experiment_name = "NewName"
        create_experiment_response = self.service.create_experiment(experiment_name)
        if not create_experiment_response.success:
            raise create_experiment_response.error

        experiment_dto: ExperimentDTO = create_experiment_response.data

        assert experiment_dto.experiment_name == experiment_name

        rename_experiment_response = self.service.rename_experiment(experiment_name, new_experiment_name)
        if not rename_experiment_response.success:
            raise rename_experiment_response.error

        assert rename_experiment_response.data.experiment_name == new_experiment_name

        delete_experiment_response = self.service.delete_experiment(new_experiment_name)
        if not delete_experiment_response.success:
            raise delete_experiment_response.error

    def test_operation_added_after_convert(self):
        experiment_name = "ConvertExperiment"
        create_experiment_response = self.service.create_experiment(experiment_name)
        if not create_experiment_response.success:
            raise create_experiment_response.error

        set_current_experiment_response = self.service.set_current_experiment(experiment_name)
        if not set_current_experiment_response.success:
            raise set_current_experiment_response.error

        # Convert image to template
        valid_image = ImageDTO(
            path=os.path.join(images_path, '109_1_8bit', '109_1_8bit.png'),
            is_dir=False
        )

        response = self.service.convert_image_to_template(valid_image)
        assert response.success
        assert response.data is not None
        generated_template: TemplateDTO = response.data

        get_current_experiment_response = self.service.get_current_experiment()
        if not get_current_experiment_response.success:
            raise get_current_experiment_response.error
        current_experiment: ExperimentDTO = get_current_experiment_response.data

        assert current_experiment.operations[0].operation_id
        assert current_experiment.operations[0].operation_type == OperationType.IMG2TMP
        assert current_experiment.operations[0].operation_input.path
        assert current_experiment.operations[0].operation_output.path == generated_template.path

        delete_experiment_response = self.service.delete_experiment(experiment_name)
        if not delete_experiment_response.success:
            raise delete_experiment_response.error

    def test_delete_operation_after_convert(self):
        experiment_name = "ConvertExperiment"
        create_experiment_response = self.service.create_experiment(experiment_name)
        if not create_experiment_response.success:
            raise create_experiment_response.error

        set_current_experiment_response = self.service.set_current_experiment(experiment_name)
        if not set_current_experiment_response.success:
            raise set_current_experiment_response.error

        # Convert image to template
        valid_image = ImageDTO(
            path=os.path.join(images_path, '109_1_8bit', '109_1_8bit.png'),
            is_dir=False
        )

        response = self.service.convert_image_to_template(valid_image)
        assert response.success
        assert response.data is not None
        generated_template: TemplateDTO = response.data

        get_current_experiment_response = self.service.get_current_experiment()
        if not get_current_experiment_response.success:
            raise get_current_experiment_response.error
        current_experiment: ExperimentDTO = get_current_experiment_response.data

        assert current_experiment.operations[0]

        delete_operation_response = self.service.delete_operation(experiment_name,
                                                                  current_experiment.operations[0].operation_id)
        if not delete_operation_response.success:
            raise delete_operation_response.error

        get_current_experiment_response = self.service.get_current_experiment()
        if not get_current_experiment_response.success:
            raise get_current_experiment_response.error
        current_experiment: ExperimentDTO = get_current_experiment_response.data

        assert current_experiment.operations == []

        delete_experiment_response = self.service.delete_experiment(experiment_name)
        if not delete_experiment_response.success:
            raise delete_experiment_response.error

    def test_set_current_experiment(self):
        experiment_name = "OldExperiment"
        create_experiment_response = self.service.create_experiment(experiment_name)
        if not create_experiment_response.success:
            raise create_experiment_response.error

        set_current_experiment_response = self.service.set_current_experiment(experiment_name)
        if not set_current_experiment_response.success:
            raise set_current_experiment_response.error

        get_current_experiment_response = self.service.get_current_experiment()
        if not get_current_experiment_response.success:
            raise get_current_experiment_response.error

        current_experiment: ExperimentDTO = get_current_experiment_response.data

        assert current_experiment.experiment_name == experiment_name

        delete_experiment_response = self.service.delete_experiment(experiment_name)
        if not delete_experiment_response.success:
            raise delete_experiment_response.error

    def tearDown(cls):
        # Clean dangling experiment
        get_all_experiments_response = cls.service.get_experiments()
        if not get_all_experiments_response.success:
            raise get_all_experiments_response.error
        experiments: list[ExperimentDTO] = get_all_experiments_response.data

        for e in experiments:
            if e.experiment_name in cls.experiment_names:
                response = cls.service.delete_experiment(e.experiment_name)
                if not response.success:
                    raise response.error


if __name__ == '__main__':
    unittest.main()
