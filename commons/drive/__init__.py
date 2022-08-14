import importlib
import logging

from commons.env import require_env

LOGGER = logging.getLogger(__name__)

def get_drive_module():
    name = require_env('drive')
    LOGGER.debug(f"Getting drive module '{name}'")
    drive = importlib.import_module(f"commons.drive.{require_env('drive')}")
    return drive