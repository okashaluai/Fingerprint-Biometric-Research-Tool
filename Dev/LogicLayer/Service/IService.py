from abc import abstractmethod

from Dev.DTOs import Response, ImageDTO, TemplateDTO


class IService:
    """ SYSTEM INTERFACE """

    @abstractmethod
    def convert_template_to_image(self, template_dto: TemplateDTO) -> Response:
        """
        This function converts imported fingerprint template to image.
        :param str template_dto: Template dto.
        :returns Response(success:bool, data:ImageDTO|None, errors:str|None)
        """
        pass

    @abstractmethod
    def convert_image_to_template(self, image_dto: ImageDTO) -> Response:
        """
        This function converts imported fingerprint image to template.
        :param str image_dto: Image dto.
        :returns Response(success:bool, data:TemplateDTO|None, errors:str|None)
        """
        pass

    @abstractmethod
    def convert_image_to_printing_object(self, image_dto: ImageDTO) -> Response:
        """
        This function converts imported fingerprint image to 3D object.
        :param str image_dto: Image dto.
        :returns Response(success:bool, data:PrintingObjectDTO|None, errors:str|None)
        """
        pass

    @abstractmethod
    def match_one_to_one(self, template1_path: str, template2_path: str) -> Response:
        """
        This function matches 2 single imported templates and returns comparison statistics.
        :param tuple[str] template1_path: First imported template path.
        :param tuple[str] template2_path: Second imported template path.
        :returns Response(success:bool, data:int|None, errors:str|None)
        """
        pass

    @abstractmethod
    def match_one_to_many(self, template_path: str, templates_dir_path: str) -> Response:
        """
        This function matches 2 single imported templates and returns comparison statistics.
        :param tuple[str] template_path: First imported template path.
        :param tuple[str] templates_dir_path: Second imported template dir path.
        :returns Response(success:bool, data:dict[str, dict[str, int]]|None, errors:str|None)
        """
        pass

    @abstractmethod
    def match_many_to_many(self, templates1_dir_path: str, templates2_dir_path: str) -> Response:
        """
        This function matches 2 single imported templates and returns comparison statistics.
        :param tuple[str] templates1_dir_path: First imported template dir path.
        :param tuple[str] templates2_dir_path: Second imported template dir path.
        :returns Response(success:bool, data:dict[str, dict[str, int]]|None, errors:str|None)
        """
        pass

    @abstractmethod
    def convert_template_to_min_map_image(self, template_dto: TemplateDTO) -> Response:
        """
        This function converts imported fingerprint template to minutae map image.
        :param str template_dto: Template dto.
        :returns Response(success:bool, data:ImageDTO|None, errors:str|None)
        """
        pass

    @abstractmethod
    def export_matching_one_to_one_csv(self, template1_path: str, template2_path: str, score,
                                       export_full_path: str) -> Response:
        """
        This function writes the results into csv file and return it
        :param str template1_path: first template (.xyt) file path
        :param str template2_path: second template (.xyt) file path
        :param int score: the matching results that is
        :param str export_full_path: where csv file will be created with the same name at the ending of the path
        returned from match function.
        :returns Response(success:bool, data:None, errors:str|None)
        """
        pass

    @abstractmethod
    def export_matching_matrix_csv(self, score_matrix, export_full_path: str) -> Response:
        """
        This function writes the results into csv file and return it
        :param dict[str, dict[str, int]] score_matrix: the matching results that is
        :param str export_full_path: where csv file will be created with the same name at the ending of the path
        returned from match function.
        :returns Response(success:bool, data:None, errors:str|None)
        """
        pass

    @abstractmethod
    def get_experiments(self) -> Response:
        """
        This function returns all existing experiments.
        :returns Response(success:bool, data:tuple[ExperimentDTO]|None, errors:str|None)
        """
        pass

    @abstractmethod
    def delete_experiment(self, experiment_name: str) -> Response:
        """
        This function deletes an experiment.
        :param str experiment_name: Experiment that will be deleted.
        :returns Response(success:bool, data:None, errors:str|None)
        """
        pass

    @abstractmethod
    def export_experiment(self, experiment_name: str, export_path: str) -> Response:
        """
        This function exports an experiment as text file.
        :param str experiment_name: Experiment that will be exported.
        :returns Response(success:bool, data:TextIO|None, errors:str|None)
        """
        pass

    @abstractmethod
    def rename_experiment(self, experiment_name: str, new_experiment_name: str) -> Response:
        """
        This function renames an experiment and returns the new renamed experiment.
        :param str experiment_name: Experiment to be renamed.
        :param str new_experiment_name: New experiment name.
        :returns Response(success:bool, data:ExperimentDTO|None, errors:str|None)
        """
        pass

    @abstractmethod
    def create_experiment(self, experiment_name: str) -> Response:
        """
        This function creates a new experiment and returns it.
        :param int experiment_name: Experiment name.
        :returns Response(success:bool, data:ExperimentDTO|None, errors:str|None)
        """
        pass

    @abstractmethod
    def set_current_experiment(self, experiment_name: str) -> Response:
        """
        This function sets the experiment with this given name to be the current experiment.
        :param str experiment_name: Existing experiment name to be the current experiment.
        :returns Response(success:bool, data:None, errors:str|None)
        """
        pass

    @abstractmethod
    def get_current_experiment(self) -> Response:
        """
        This function returns the current experiment.
        :returns Response(success:bool, data:ExperimentDTO, errors:str|None)
        """
        pass

    @abstractmethod
    def delete_operation(self, experiment_name: str, operation_id: int) -> Response:
        """
        This function deletes an operation with the given id.
        :returns Response(success:bool, data:None, errors:str|None)
        """
        pass
