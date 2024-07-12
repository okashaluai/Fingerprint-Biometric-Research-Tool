from Dev.DTOs import PrintingObjectDTO
from Dev.LogicLayer.LogicObjects.Asset import Asset


class PrintingObject(Asset):
    def __init__(self, path: str, is_dir):
        super().__init__(path, is_dir)

    def to_dto(self) -> PrintingObjectDTO:
        return PrintingObjectDTO(path=self.path, is_dir=self.is_dir)
