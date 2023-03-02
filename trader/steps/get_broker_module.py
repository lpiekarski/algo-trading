import logging
from trader import broker_apis

LOGGER = logging.getLogger(__name__)


def get_broker_module(broker, **kwargs):
    broker_module = broker_apis.get_broker_module(broker)
    return dict(broker_module=broker_module)
