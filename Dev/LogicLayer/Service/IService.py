from abc import abstractmethod

from Dev.DTOs import Response, ImageDTO, TemplateDTO


class IService:
    """ SYSTEM INTERFACE """

    @abstractmethod
    def convert_template_to_image(self, experiment_name: str, template_dto: TemplateDTO) -> Response:
        """
        This function converts imported fingerprint template to image.
        :param str experiment_name: Experiment's name.
                :param str template_dto: Template dto.
        :returns Response(success:bool, data:ImageDTO|None, errors:str|None)
        """
        pass

    @abstractmethod
    def convert_image_to_template(self, experiment_name: str, image_dto: ImageDTO) -> Response:
        """
        This function converts imported fingerprint image to template.
        :param str experiment_name: Experiment's name.
        :param str image_dto: Image dto.
        :returns Response(success:bool, data:TemplateDTO|None, errors:str|None)
        """
        pass

    @abstractmethod
    def convert_image_to_printing_object(self, experiment_name: str, image_dto: ImageDTO) -> Response:
        """
        This function converts imported fingerprint image to 3D object.
        :param str experiment_name: Experiment's name.
        :param str image_dto: Image dto.
        :returns Response(success:bool, data:PrintingObjectDTO|None, errors:str|None)
        """
        pass

    @abstractmethod
    def match(self, experiment_name: str, templates_path1: tuple[str], templates_path2: tuple[str]) -> Response:
        """
        This function matches 2 groups of imported templates and returns comparison statistics.
                :param str experiment_name: Experiment's name.
        :param tuple[str] templates_path1: First imported template group.
        :param tuple[str] templates_path2: Second imported template group.
        :returns Response(success:bool, data:int|dict[str, int]|dict[str, dict[str, int]]|None, errors:str|None)
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
    def export_experiment(self, experiment_name: str) -> Response:
        """
        This function exports an experiment as text file.
        :param str experiment_name: Experiment that will be exported.
        :returns Response(success:bool, data:TextIO|None, errors:str|None)
        """
        pass

    @abstractmethod
    def rename_experiment(self, experiment_name: str, new_name: str) -> Response:
        """
        This function renames an experiment and returns the new renamed experiment.
        :param str experiment_name: Experiment to be renamed.
        :param str new_name: New experiment name.
        :returns Response(success:bool, data:ExperimentDTO|None, errors:str|None)
        """
        pass

    @abstractmethod
    def create_experiment(self, experiment_name: str) -> Response:
        """
        This function creates a new experiment and returns it.
        :param str experiment_name: Experiment name.
        :returns Response(success:bool, data:ExperimentDTO|None, errors:str|None)
        """
        pass

    @abstractmethod
    def set_current_experiment(self, experiment_name: str) -> Response:
        """
        This function sets the experiment with this name to be the current experiment.
        :param str experiment_name: Existing experiment name to be the current experiment.
        :returns Response(success:bool, data:None, errors:str|None)
        """
        pass

    @abstractmethod
    def get_current_experiment_name(self) -> Response:
        """
        This function returns the current experiment.
        :returns Response(success:bool, data:str, errors:str|None)
        """
        pass
