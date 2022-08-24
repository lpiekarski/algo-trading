import importlib
import logging

from commons.env import getenv

LOGGER = logging.getLogger(__name__)

def get_drive_module(name=None):
    if name is None:
        name = getenv('drive')
    LOGGER.debug(f"Getting drive module '{name}'")
    drive = importlib.import_module(f"commons.drive.{name}")
    return drive