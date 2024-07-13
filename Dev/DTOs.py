import os.path
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from Dev.Enums import OperationType
from Dev.Utils import Interface


class IDto(Interface):
    pass


@dataclass(frozen=True)
class Response:
    """
    This data class used in communication between logic layer and presentation layer
    to provide comprehensive and robust error management.
    :param bool success: True upon success, False else.
    :param object|None data: Can be any object when we return value, else None.
    :param str|None error: Non-empty error message upon failure, else None.
    """
    success: bool
    data: object | None
    error: str | None


@dataclass(frozen=True)
class AssetDTO(IDto):
    path: str
    is_dir: bool


@dataclass(frozen=True)
class TemplateDTO(AssetDTO):
    def __eq__(self, other):
        if self.is_dir != other.is_dir:
            return False

        def get_templates_base_names(path: str):
            template_names = []
            for f in os.listdir(path):
                base_name = Path(f).stem
                if base_name not in template_names:
                    template_names.append(base_name)
            return template_names

        this_templates_base_names = get_templates_base_names(self.path)
        other_templates_base_names = get_templates_base_names(other.path)

        if this_templates_base_names.sort() != other_templates_base_names.sort():
            return False

        for t_name in this_templates_base_names:
            with open(os.path.join(self.path, f"{t_name}.min")) as f:
                f1_min_content = f.readlines()
            with open(os.path.join(self.path, f"{t_name}.xyt")) as f:
                f1_xyt_content = f.readlines()

            if not (os.path.exists(os.path.join(other.path, f"{t_name}.min"))
                    and os.path.join(other.path, f"{t_name}.xyt")):
                return False

            with open(os.path.join(other.path, f"{t_name}.min")) as f:
                f2_min_content = f.readlines()
            with open(os.path.join(other.path, f"{t_name}.xyt")) as f:
                f2_xyt_content = f.readlines()

            if not (f1_min_content.sort() == f2_min_content.sort() and f1_xyt_content.sort() == f2_xyt_content.sort()):
                return False

        return True


@dataclass(frozen=True)
class ImageDTO(AssetDTO):
    pass


@dataclass(frozen=True)
class PrintingObjectDTO(AssetDTO):
    pass


@dataclass(frozen=False)
class OperationDTO(IDto):
    operation_id: str
    operation_type: OperationType
    operation_input: AssetDTO
    operation_output: AssetDTO
    operation_datetime: datetime


@dataclass(frozen=False)
class ExperimentDTO(IDto):
    operations: list[OperationDTO]
    experiment_name: str
    experiment_datetime: datetime
