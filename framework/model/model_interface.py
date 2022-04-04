from abc import ABC, abstractmethod


class ModelInterface(ABC):
    @abstractmethod
    def predict(self, *args, **kwargs):
        pass
