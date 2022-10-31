import importlib
import logging

from commons.env import getenv
from commons.exceptions import BotError

LOGGER = logging.getLogger(__name__)

def get_drive_module(name=None):
    if name is None:
        name = getenv('drive')
    LOGGER.debug(f"Active drive module '{name}'")
    try:
        return importlib.import_module(f"commons.drive.{name}")
    except ImportError:
        raise BotError(f"No such drive: {name}")