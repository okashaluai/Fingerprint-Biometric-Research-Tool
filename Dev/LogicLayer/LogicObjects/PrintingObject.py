from Dev.DTOs import PrintingObjectDTO
from Dev.DataAccessLayer.DAOs import PrintingObjectDAO
from Dev.LogicLayer.LogicObjects.Asset import Asset
import os


class PrintingObject(Asset):
    def __init__(self, path: str, is_dir):
        super().__init__(path, is_dir)

    def to_dto(self) -> PrintingObjectDTO:
        return PrintingObjectDTO(path=self.path, date=self.date, is_dir=self.is_dir)

    def to_dao(self) -> PrintingObjectDAO:
        raise NotImplementedError

    def finalize_path(self, final_destination_path: str):
        if os.path.exists(final_destination_path) and os.path.isdir(final_destination_path):
            super().path = final_destination_path
        else:
            raise Exception(f'Final Destination was not found {final_destination_path} does not exist')
