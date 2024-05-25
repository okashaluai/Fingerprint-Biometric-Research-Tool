from abc import ABCMeta


class Interface(metaclass=ABCMeta):
    """ This is a mix of Interface and Abstract Class that supports multiple inheritance """
    pass


class Singleton(type):
    """ This can be used as a baseclass to declare that certain class is a singleton """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    def get_instance(cls):
        return cls._instances[cls]
