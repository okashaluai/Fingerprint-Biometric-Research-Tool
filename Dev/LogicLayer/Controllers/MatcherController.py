from Dev.LogicLayer.Matcher.Matcher import Matcher
from Dev.Utils import Singleton


class MatcherController(metaclass=Singleton):

    def __init__(self):
        self.matcher = Matcher()

    def match_templates(self, first_set_path: tuple[str], second_set_path: tuple[str]) -> (int |
                                                                                           dict[str, int] |
                                                                                           dict[str, dict[str, int]]):
        if len(first_set_path) == 1 and len(second_set_path) == 1:
            return self.matcher.match_one_to_one(first_set_path[0], second_set_path[0])

        elif len(first_set_path) == 1 and len(second_set_path) > 1:
            return self.matcher.match_one_to_many(first_set_path[0], second_set_path)

        elif len(second_set_path) == 1 and len(first_set_path) > 1:
            return self.matcher.match_one_to_many(second_set_path[0], first_set_path)

        elif len(first_set_path) > 1 and len(second_set_path) > 1:
            return self.matcher.match_many_to_many(first_set_path, second_set_path)

        else:
            raise Exception("Missing template paths set!")
