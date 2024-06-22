from Dev.LogicLayer.Matcher.IMatcher import IMatcher
from Dev.NBIS.NBIS import match_templates
from Dev.Utils import Singleton


class Matcher(IMatcher, metaclass=Singleton):

    def match_one_to_one(self, template1_path: str, template2_path: str) -> int:
        matching_score = match_templates(template1_path, template2_path)
        return matching_score

    def match_one_to_many(self, template_path: str, templates_path: list[str]) -> dict[str, dict[str, int]]:
        matrix_score = dict()  # <Key: template1_path, Value: <Key: template2_path, Value: score>>

        scores_dic = dict()  # <Key: template2_path, Value: score>
        for tp2 in templates_path:
            scores_dic[tp2] = match_templates(template_path, tp2)
        matrix_score[template_path] = scores_dic

        return matrix_score

    def match_many_to_many(self, templates1_path: list[str], templates2_path: list[str]) -> dict[str, dict[str, int]]:
        matrix_score = dict()  # <Key: template1_path, Value: <Key: template2_path, Value: score>>

        for tp1 in templates1_path:
            scores_dic = dict()  # <Key: template2_path, Value: score>
            for tp2 in templates2_path:
                scores_dic[tp2] = match_templates(tp1, tp2)
            matrix_score[tp1] = scores_dic

        return matrix_score
