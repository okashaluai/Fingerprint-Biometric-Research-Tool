from dataclasses import dataclass
from typing import TextIO
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
    id: int
    path: str
    date: float


@dataclass(frozen=True)
class TemplateDTO(AssetDTO):
    # TODO: we may need to use data structure instead of text file
    min_file: TextIO
    xyt_file: TextIO


@dataclass(frozen=True)
class ImageDTO(AssetDTO):
    # we only need the image path not the image itself.
    # more params to add later here...
    pass


@dataclass(frozen=True)
class PrintingObjectDTO(AssetDTO):
    # we only need the stl path not the file itself.
    # more params to add later here...
    pass


@dataclass(frozen=True)
class OperationDTO(IDto):
    id: int
    experiment_id: int
    operation_type: OperationType
    input: AssetDTO
    output: AssetDTO
    date: float


@dataclass(frozen=True)
class ExperimentDTO(IDto):
    id: int
    name: str
    date: float
    operations: tuple[OperationDTO]

