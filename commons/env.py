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


class Env:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.old_values = None

    def __enter__(self):
        self.old_values = {k: getenv(k) for k, _ in self.kwargs.items()}
        for k, v in self.kwargs.items():
            os.environ[k] = v

    def __exit__(self, exc_type, exc_val, exc_tb):
        for k, v in self.old_values.items():
            if v is None:
                del os.environ[k]
            else:
                os.environ[k] = v


class DefaultEnv:
    CACHE_DIR = './.cache'
    TEMP_DIR = './.tmp'
    drive = 'local'
    GIT_DRIVE_MAX_FILE_SIZE = '100000000'
