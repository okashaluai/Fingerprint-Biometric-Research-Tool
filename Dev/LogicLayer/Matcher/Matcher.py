from Dev.LogicLayer.Matcher.IMatcher import IMatcher
from Dev.NBIS.NBIS import match_templates
from Dev.Utils import Singleton


class Matcher(IMatcher, metaclass=Singleton):

    def match_one_to_one(self, template1_path: str, template2_path: str) -> int:
        matching_score = match_templates(template1_path, template2_path)
        return matching_score

    def match_one_to_many(self, template_path: str, templates_path: tuple[str]) -> dict[str, int]:
        scores_dic = dict()  # <Key: other_template_path, Value: score>
        for tp in templates_path:
            scores_dic[tp] = match_templates(template_path, tp)
        return scores_dic

    def match_many_to_many(self, templates1_path: tuple[str], templates2_path: tuple[str]) -> dict[str, dict[str, int]]:
        matrix_score = dict()  # <Key: template1_path, Value: <Key: template2_path, Value: score>>

        for tp1 in templates1_path:
            scores_dic = dict()  # <Key: template2_path, Value: score>
            for tp2 in templates2_path:
                scores_dic[tp2] = match_templates(tp1, tp2)
            matrix_score[tp1] = scores_dic

        return matrix_score
