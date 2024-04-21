from abc import abstractmethod

from Dev.LogicLayer.LogicObjects.Template import Template
from Dev.Utils import Interface


class IMatcher(Interface):
    @abstractmethod
    def match_one_to_one(self, template1: Template, template2: Template) -> str:
        pass

    @abstractmethod
    def match_one_to_many(self, template: Template, templates: tuple[Template]) -> str:
        pass

    @abstractmethod
    def match_many_to_many(self, templates1: tuple[Template], templates2: tuple[Template]) -> str:
        pass
