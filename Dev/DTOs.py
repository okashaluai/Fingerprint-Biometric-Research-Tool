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
    id: int | None
    path: str
    date: datetime


@dataclass(frozen=True)
class TemplateDTO(AssetDTO):
    pass


@dataclass(frozen=True)
class ImageDTO(AssetDTO):
    pass


@dataclass(frozen=True)
class PrintingObjectDTO(AssetDTO):
    pass


@dataclass(frozen=False)
class OperationDTO(IDto):
    operation_id: int | None
    operation_type: OperationType
    operation_input: AssetDTO
    operation_output: AssetDTO
    operation_date: datetime


@dataclass(frozen=False)
class ExperimentDTO(IDto):
    operations: list[OperationDTO]
    experiment_id: int | None
    experiment_name: str
    experiment_date: datetime
