import logging.config
import os

path_to_conf = os.path.dirname(os.path.realpath(__file__))
logging.config.fileConfig(f'{path_to_conf}/logging.conf', disable_existing_loggers=False)

logger = logging.getLogger(__name__)
log_factory = logging.getLogRecordFactory()


def record_factory(*args, **kwargs):
    record = log_factory(*args, **kwargs)
    record.project = os.environ.get("PROJECT", None)
    return record


logging.setLogRecordFactory(record_factory)
