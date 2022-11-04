import os

__all__ = ["getenv", "require_env"]

from commons.exceptions import ArgumentError

def getenv(name, default=None):
    value = os.getenv(name)
    if value is None:
        if hasattr(DefaultEnv, name):
            return getattr(DefaultEnv, name)
        return default
    return value

def require_env(name):
    value = os.getenv(name)
    if value is None:
        if hasattr(DefaultEnv, name):
            return getattr(DefaultEnv, name)
        raise ArgumentError(f"Missing environment variable '{name}'")
    return value

class DefaultEnv:
    CACHE_DIR = './.cache'
    TEMP_DIR = './.tmp'
    drive = 'local'
    GIT_DRIVE_MAX_FILE_SIZE = '100000000'