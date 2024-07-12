from dataclasses import dataclass
from datetime import datetime

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
        f1_min_content = []
        f1_xyt_content = []
        f2_min_content = []
        f2_xyt_content = []

        with open(self.path.join('.min')) as f:
            f1_min_content = f.readlines()

        with open(self.path.join('.xyt')) as f:
            f1_xyt_content = f.readlines()

        with open(other.path.join('.min')) as f:
            f2_min_content = f.readlines()

        with open(other.path.join('.xyt')) as f:
            f2_xyt_content = f.readlines()

        return (f1_min_content.sort() == f2_min_content.sort()) and (f1_xyt_content.sort() == f2_xyt_content.sort())


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
