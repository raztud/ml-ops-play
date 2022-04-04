import json
import logging
from typing import Dict

from framework.monitoring.metric import Metric

logger = logging.getLogger(__name__)


class LoggerMetric(Metric):
    def add_metric(self, name, value, tags: Dict = None):
        data = {
            "name": name,
            "value": value,
            "tags": tags,
        }

        logging.info(json.dumps(data))

    def add_count(self, name, total=1, tags: Dict = None):
        data = {
            "name": name,
            "total": total,
            "tags": tags,
        }

        logging.info(json.dumps(data))
