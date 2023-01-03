import importlib
import logging
from core.env import require_env
from core.exceptions import InvalidDriveTypeError

LOGGER = logging.getLogger(__name__)


def get_drive_module(name=None):
    if name is None:
        name = require_env('drive')
    try:
        return importlib.import_module(f"core.drive.{name}")
    except ImportError:
        raise InvalidDriveTypeError(f"No such drive: {name}")
