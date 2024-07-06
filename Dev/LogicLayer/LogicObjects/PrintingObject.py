from Dev.DTOs import PrintingObjectDTO
from Dev.DataAccessLayer.DAOs import PrintingObjectDAO
from Dev.LogicLayer.LogicObjects.Asset import Asset
import os


class PrintingObject(Asset):
    def __init__(self, path: str):
        super().__init__(path)

    def to_dto(self) -> PrintingObjectDTO:
        return PrintingObjectDTO(id=0, path=self.path, date=self.date)

    def to_dao(self) -> PrintingObjectDAO:
        raise NotImplementedError

    def finalize_path(self, final_destination_path: str):
        if os.path.exists(final_destination_path) and os.path.isdir(final_destination_path):
            super().path = final_destination_path
        else:
            raise Exception(f'Final Destination was not found {final_destination_path} does not exist')
