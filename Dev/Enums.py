from enum import Enum


class OperationType(Enum):
    """
    Enum class for operation type.
    :param TMP_IMG: Template to Image.
    :param TMP_IMG: Image to Template.
    :param TMP_IMG: Image to Printing Object.
    """
    TMP2IMG: str = 'TMP2IMG'
    TMPs2IMGs: str = 'TMPs2IMGs'
    IMG2TMP: str = 'IMG2TMP'
    IMGs2TMPs: str = 'IMGs2TMPs'
    IMG2POBJ: str = 'IMG2POBJ'
    IMGs2POBJs: str = 'IMGs2POBJs'
