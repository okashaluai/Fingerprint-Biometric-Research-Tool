from Dev.DTOs import PrintingObjectDTO
from Dev.DataAccessLayer.DAOs import PrintingObjectDAO
from Dev.LogicLayer.LogicObjects.Asset import Asset


class PrintingObject(Asset):
    def __init__(self, path: str):
        super().__init__(path)

    def to_dto(self) -> PrintingObjectDTO:
        return PrintingObjectDTO(id=0, path=self.path, date=self.date)

    def to_dao(self) -> PrintingObjectDAO:
        raise NotImplementedError
