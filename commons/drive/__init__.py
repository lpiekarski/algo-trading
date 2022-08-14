import importlib
import logging

from commons.env import getenv

LOGGER = logging.getLogger(__name__)

def get_drive_module():
    name = getenv('drive', 'local')
    LOGGER.debug(f"Getting drive module '{name}'")
    drive = importlib.import_module(f"commons.drive.{name}")
    return drive