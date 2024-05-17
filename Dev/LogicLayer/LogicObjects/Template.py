from Dev.DTOs import TemplateDTO
from Dev.DataAccessLayer.DAOs import TemplateDAO
from Dev.LogicLayer.LogicObjects.Asset import Asset
from Dev.LogicLayer.LogicObjects.ILogicObject import ILogicObject
import os

class Template(Asset):
    def __init__(self, path):
        super().__init__(path)

    def to_dto(self) -> TemplateDTO:
        raise NotImplementedError

    def to_dao(self) -> TemplateDAO:
        raise NotImplementedError

    def __eq__(self, other):
        f1_min_content = []
        f1_xyt_content = []
        f2_min_content = []
        f2_xyt_content = []
        
        with open(self.__path.join('.min')) as f:
            f1_min_content = f.readlines()

        with open(self.__path.join('.xyt')) as f:
            f1_xyt_content = f.readlines()
        
        with open(other.__path.join('.min')) as f:
            f2_min_content = f.readlines()

        with open(other.__path.join('.xyt')) as f:
            f2_xyt_content = f.readlines()

        return (f1_min_content.sort() == f2_min_content.sort()) and (f1_xyt_content.sort() == f2_xyt_content.sort())