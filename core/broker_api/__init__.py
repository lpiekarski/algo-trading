import importlib
import logging
from core.env import require_env

LOGGER = logging.getLogger(__name__)


def get_broker_module(name=None):
    if name is None:
        name = require_env('broker')
    LOGGER.debug(f"Getting broker module '{name}'")
    broker = importlib.import_module(f"core.broker_api.{name}")
    return broker
