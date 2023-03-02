import yaml
import logging
from typing import Union

from core.drivepath import Drivepath, cache

__all__ = ["download_broker_config"]

LOGGER = logging.getLogger(__name__)


def download_broker_config(drivepath: Union[Drivepath, str]):
    file, _ = cache(drivepath)
    with open(file, 'r') as f:
        return yaml.load(f, yaml.CLoader)
