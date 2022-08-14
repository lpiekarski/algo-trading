import os

__all__ = ["getenv", "require_env"]

from commons.exceptions import ArgumentError

def getenv(name, default=None):
    value = os.getenv(name)
    if value is None:
        return default
    return value

def require_env(name):
    value = os.getenv(name)
    if value is None:
        raise ArgumentError(f"Missing environment variable '{name}'")
    return value