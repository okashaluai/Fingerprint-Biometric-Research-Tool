from Dev.DTOs import ImageDTO
from Dev.DataAccessLayer.DAOs import ImageDAO
from Dev.LogicLayer.LogicObjects.Asset import Asset


class Image(Asset):
    def __init__(self):
        super().__init__()

    def to_dto(self) -> ImageDTO:
        raise NotImplementedError

    def to_dao(self) -> ImageDAO:
        raise NotImplementedError