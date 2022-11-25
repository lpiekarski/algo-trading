import importlib
import logging

from commons.configparams import Config

LOGGER = logging.getLogger(__name__)


def get_broker_module(name=None):
    if name is None:
        name = Config.require_param('broker')
    LOGGER.debug(f"Getting broker module '{name}'")
    broker = importlib.import_module(f"commons.broker_api.{name}")
    return broker
