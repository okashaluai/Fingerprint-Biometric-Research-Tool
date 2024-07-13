import os
import unittest

from Dev.DTOs import ExperimentDTO
from Dev.LogicLayer.Service.Service import Service
from TestUtils import templates_path


class MatchTemplates(unittest.TestCase):
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

    def test_match_one_to_one(self):
        first_template_path = os.path.join(templates_path, '109_1_8bit', '109_1_8bit.xyt')
        second_template_path = os.path.join(templates_path, '109_2_8bit', '109_2_8bit.xyt')

        response = self.service.match_one_to_one(first_template_path, second_template_path)
        assert response.success

        score = response.data

        assert score is not None
        assert score == 27

    def test_match_one_to_one_invalid_template(self):
        first_template_path = os.path.join(templates_path, '109_1_8bit', '109_1_8bit.xyt')
        second_template_path = os.path.join(templates_path, '109_2_8bit', 'bla.xyt')

        response = self.service.match_one_to_one(first_template_path, second_template_path)
        assert not response.success

    def test_match_one_to_many(self):
        first_template_path = os.path.join(templates_path, '109_1_8bit', '109_1_8bit.xyt')
        second_template_dir = os.path.join(templates_path, 'many_templates')

        response = self.service.match_one_to_many(first_template_path, second_template_dir)
        assert response.success

        score = response.data

        assert score is not None

        assert score[first_template_path][os.path.join(second_template_dir, '109_2_8bit.xyt')] == 27
        assert score[first_template_path][os.path.join(second_template_dir, '109_3_8bit.xyt')] == 100

    def test_match_one_to_many_invalid_template(self):
        first_template_path = os.path.join(templates_path, '109_1_8bit', 'bla.xyt')
        second_template_dir = os.path.join(templates_path, 'many_templates')

        response = self.service.match_one_to_many(first_template_path, second_template_dir)
        assert not response.success

    def test_match_many_to_many(self):
        template_dir = os.path.join(templates_path, 'many_templates')

        response = self.service.match_many_to_many(template_dir, template_dir)
        assert response.success

        score = response.data

        assert score is not None

        t_109_2_path = os.path.join(template_dir, '109_2_8bit.xyt')
        t_109_3_path = os.path.join(template_dir, '109_3_8bit.xyt')

        assert score[t_109_2_path][t_109_2_path] == 253
        assert score[t_109_2_path][t_109_3_path] == 32
        assert score[t_109_3_path][t_109_3_path] == 420
        assert score[t_109_3_path][t_109_2_path] == 32

    def test_match_many_to_many_invalid_template(self):
        template_dir = os.path.join(templates_path, 'bla')

        response = self.service.match_many_to_many(template_dir, template_dir)
        assert not response.success

    @classmethod
    def tearDownClass(cls):
        response = cls.service.delete_experiment(cls.experiment_name)
        if not response.success:
            raise response.error


if __name__ == '__main__':
    unittest.main()
