from abc import abstractmethod

from Dev.Utils import Interface


class IMatcher(Interface):
    @abstractmethod
    def match_one_to_one(self, template1_path: str, template2_path: str) -> str:
        pass

    @abstractmethod
    def match_one_to_many(self, template_path: str, templates_path: tuple[str]) -> dict[str, int]:
        pass

    @abstractmethod
    def match_many_to_many(self, templates1_path: tuple[str], templates2_path: tuple[str]) -> dict[str, dict[str, int]]:
        pass
