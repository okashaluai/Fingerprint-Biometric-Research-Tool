from enum import Enum


class OperationType(Enum):
    """
    Enum class for operation type.
    :param TMP_IMG: Template to Image.
    :param TMP_IMG: Image to Template.
    :param TMP_IMG: Image to Printing Object.
    """
    TMP_IMG: int = 1
    IMG_TMP: int = 2
    IMG_POBJ: int = 3
