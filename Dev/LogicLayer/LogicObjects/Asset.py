import os

from Dev.DTOs import AssetDTO
from Dev.LogicLayer.LogicObjects.ILogicObject import ILogicObject


class Asset(ILogicObject):
    def __init__(self, path: str, is_dir: bool):
        self.path = path
        self.is_dir: bool = is_dir

    def to_dto(self) -> AssetDTO:
        return AssetDTO(self.path, self.is_dir)

    def finalize_path(self, final_destination_path: str = None):
        if final_destination_path is None:
            self.path = os.path.abspath(self.path)
        else:
            template_file_name = os.path.basename(self.path)
            if os.path.exists(final_destination_path) and os.path.isdir(final_destination_path):
                if self.is_dir:
                    self.path = os.path.abspath(final_destination_path)
                else:
                    self.path = os.path.abspath(os.path.join(final_destination_path, template_file_name))
            else:
                raise Exception(f'Final Destination was not found {final_destination_path} does not exist')

