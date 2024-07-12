from abc import abstractmethod
from Dev.DTOs import IDto
from Dev.Utils import Interface


class ILogicObject(Interface):
    """
    Interface for logic layer objects.
    """

    @abstractmethod
    def to_dto(self) -> IDto:
        """
        Converts the logic object to dto.
        :returns dto: Dto of the logic layer object.
        """
        pass
