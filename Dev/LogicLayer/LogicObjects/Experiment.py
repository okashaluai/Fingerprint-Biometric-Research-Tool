from Dev.DTOs import ExperimentDTO
from Dev.DataAccessLayer.DAOs import ExperimentDAO
from Dev.LogicLayer.LogicObjects.ILogicObject import ILogicObject


class Experiment(ILogicObject):
    def __init__(self):
        pass

    def to_dto(self) -> ExperimentDTO:
        raise NotImplementedError

    def to_dao(self) -> ExperimentDAO:
        raise NotImplementedError
