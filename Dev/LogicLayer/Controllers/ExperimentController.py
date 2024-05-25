from Dev.LogicLayer.LogicObjects.Operation import Operation
from Dev.Utils import Singleton


class ExperimentController(metaclass=Singleton):

    @staticmethod
    def add_operation(operation: Operation) -> Operation:
        # TODO - need to save the added operation then return the new operation which contains the new input and
        #  output paths.
        return operation
