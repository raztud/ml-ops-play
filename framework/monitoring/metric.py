import os
from abc import ABC, abstractmethod
from typing import Dict


class Metric(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def add_metric(self, name, value, tags: Dict = None):
        pass

    @abstractmethod
    def add_count(self, name, total=1, tags: Dict = None):
        pass

    @staticmethod
    def get_default_tags():
        return {"project": os.environ.get("PROJECT", "default")}
