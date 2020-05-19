from copy import deepcopy


class ToDictMixin:
    def to_dict(self):
        data = deepcopy(self.__dict__)
        data.pop('local_alerts', '')
        return data

    def __repr__(self):
        return str(self.__dict__)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
