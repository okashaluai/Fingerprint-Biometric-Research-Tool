from Dev.LogicLayer.LogicObjects.Template import Template
from Dev.LogicLayer.Matcher.IMatcher import IMatcher


class Matcher(IMatcher):
    def __init__(self):
        pass

    def match_one_to_one(self, template1: Template, template2: Template) -> str:
        raise NotImplementedError

    def match_one_to_many(self, template: Template, templates: tuple[Template]) -> str:
        raise NotImplementedError

    def match_many_to_many(self, templates1: tuple[Template], templates2: tuple[Template]) -> str:
        raise NotImplementedError
