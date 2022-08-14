import importlib

from commons.env import require_env

def get_model_module(name: str=None):
    if name is None:
        name = require_env("model")
    return importlib.import_module(f"model.predictors.{name}")