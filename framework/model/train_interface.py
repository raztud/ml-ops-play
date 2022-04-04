import io
from abc import ABC, abstractmethod

from framework.model.saving_configuration import SavingConfiguration


class TrainInterface(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def load_data(self):
        pass

    @staticmethod
    def save_buffer(model: io.BufferedIOBase, config: SavingConfiguration):
        config.saver_object.save_buffer(model, config.path)
