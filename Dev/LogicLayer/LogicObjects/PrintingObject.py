from Dev.DTOs import PrintingObjectDTO
from Dev.DataAccessLayer.DAOs import PrintingObjectDAO
from Dev.LogicLayer.LogicObjects.Asset import Asset


class PrintingObject(Asset):
    def __init__(self):
        super().__init__()

    def to_dto(self) -> PrintingObjectDTO:
        raise NotImplementedError

    def to_dao(self) -> PrintingObjectDAO:
        raise NotImplementedError
