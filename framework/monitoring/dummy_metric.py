from typing import Dict

from framework.monitoring.metric import Metric


class DummyMetric(Metric):
    def add_metric(self, name, value, tags: Dict = None):
        print(name, value, tags)

    def add_count(self, name, total=1, tags: Dict = None):
        print(name, total, tags)
