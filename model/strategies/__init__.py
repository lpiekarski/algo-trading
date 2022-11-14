import importlib
import os
from typing import Union

from commons.drivepath import Drivepath, from_string


def get_strategy_module(drivepath: Union[Drivepath, str] = None):
    drivepath = from_string(drivepath)
    return importlib.import_module(
        f"model.strategies.{os.path.basename(drivepath.path)}")
