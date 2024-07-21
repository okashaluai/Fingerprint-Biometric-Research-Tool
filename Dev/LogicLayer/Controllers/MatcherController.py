import csv
import os
from pathlib import Path

from Dev.LogicLayer.Matcher.Matcher import Matcher
from Dev.Utils import Singleton
from Dev.DataAccessLayer.FILESYSTEM import FILESYSTEM

class MatcherController(metaclass=Singleton):

    def __init__(self):
        self.matcher = Matcher()

    def match_one_to_one(self, src_template_path: str, target_template_path: str) -> int:
        matching_score = self.matcher.match_one_to_one(src_template_path, target_template_path)
        return matching_score

    def match_one_to_many(self, src_template_path: str, target_templates_dir_path: str) -> dict[str, dict[str, int]]:
        templates_path = [os.path.join(target_templates_dir_path, template) for template in os.listdir(target_templates_dir_path)]
        matching_score = self.matcher.match_one_to_many(src_template_path, templates_path)
        return matching_score

    def match_many_to_many(self, src_templates_dir_path: str, target_templates_dir_path: str) -> dict[str, dict[str, int]]:
        templates1_path = [os.path.join(src_templates_dir_path, template) for template in os.listdir(src_templates_dir_path)]
        templates2_path = [os.path.join(target_templates_dir_path, template) for template in os.listdir(target_templates_dir_path)]

        matching_score = self.matcher.match_many_to_many(templates1_path, templates2_path)
        return matching_score

    def write_matrix_score_as_csv(self, score_matrix, csv_path: str) -> None:
        with open(csv_path, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            scores_row_entry = dict()

            for i, t1_path in enumerate(score_matrix.keys()):
                row_entry = []
                scores_row_entry[i + 1] = []

                for t2_path in score_matrix[t1_path].keys():
                    row_entry.append(Path(t2_path).stem)
                    scores_row_entry[i + 1].append(score_matrix[t1_path][t2_path])

                if i == 0:
                    row_entry = [''] + row_entry
                elif i < len(score_matrix.keys()):
                    row_entry = [Path(list(score_matrix.keys())[i - 1]).stem] + scores_row_entry[i]

                writer.writerow(row_entry)

            last_row = [Path(list(score_matrix.keys())[i]).stem] + scores_row_entry[i + 1]
            writer.writerow(last_row)

    def write_one_to_one_score_as_csv(self, src_template_path: str, target_template_path: str, score: int,
                                      csv_path: str) -> None:
        matrix = dict()
        matrix[src_template_path] = dict()
        matrix[src_template_path][target_template_path] = score

        self.write_matrix_score_as_csv(matrix, csv_path)
