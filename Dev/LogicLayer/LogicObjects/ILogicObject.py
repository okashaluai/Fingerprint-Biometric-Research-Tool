from abc import abstractmethod

from Dev.DTOs import IDto
from Dev.DataAccessLayer.DAOs import IDao
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

    @abstractmethod
    def to_dao(self) -> IDao:
        """
        Converts the logic object to dao.
        :returns dto: Dao of the logic layer object.
        """
        pass
