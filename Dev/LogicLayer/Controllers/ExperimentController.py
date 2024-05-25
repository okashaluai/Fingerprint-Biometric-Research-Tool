from Dev.LogicLayer.LogicObjects.Operation import Operation
from Dev.Utils import Singleton


class ExperimentController(metaclass=Singleton):
    def __init__(self):
        pass

    def add_operation(self, operation: Operation) -> Operation:
        # TODO - need to save the added operation then return the new operation which contains the new input and
        #  output paths.
        return operation
