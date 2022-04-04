import logging.config
import os

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

logger = logging.getLogger(__name__)
log_factory = logging.getLogRecordFactory()


def record_factory(*args, **kwargs):
    record = log_factory(*args, **kwargs)
    record.project = os.environ.get("PROJECT", None)
    return record


logging.setLogRecordFactory(record_factory)
