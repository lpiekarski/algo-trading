import importlib
import logging
from commons.env import require_env
from commons.exceptions import InvalidDriveTypeError

LOGGER = logging.getLogger(__name__)


def get_drive_module(name=None):
    if name is None:
        name = require_env('drive')
    try:
        return importlib.import_module(f"commons.drive.{name}")
    except ImportError:
        raise InvalidDriveTypeError(f"No such drive: {name}")
