import io
from abc import ABC, abstractmethod


class StorageObjectInterface(ABC):
    @abstractmethod
    def save(self, *args, **kwargs):
        pass

    @abstractmethod
    def save_buffer(self, *args, **kwargs):
        pass

    @abstractmethod
    def retrieve(self, *args, **kwargs) -> io.BufferedIOBase:
        pass
