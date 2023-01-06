import os
from core.exceptions import ArgumentError

__all__ = ["require_env", "set_env_from_file", "TempEnv"]

DEFAULT_ENV = dict(
    CACHE_DIR="./.cache",
    TEMP_DIR="./.tmp",
    DRIVE="local",
    GIT_DRIVE_MAX_FILE_SIZE="100000000"
)


def require_env(name: str) -> str:
    """Get environmental variable with given name. Raise "ArgumentError" if the variable has no value set."""
    value = os.getenv(name)
    if value is None:
        raise ArgumentError(f"Missing environment variable '{name}'")
    return value


def set_env_from_file(filename: str) -> dict:
    """
    Read env file consisting of "var_name=value" lines. Store environmental variables present in that file
    directly to os.environ.

    Returns a dictionary of all variables read from the file
    """
    result = {}
    with open(filename, "r") as f:
        lines = f.readlines()
        # Filter out empty lines and comments
        lines = list(filter(lambda line: line != "", lines))
        lines = list(filter(lambda line: not line.isspace(), lines))
        lines = list(filter(lambda line: not line.strip().startswith("#"), lines))
        for entry in lines:
            entry_split = entry.split("=", 1)
            if len(entry_split) != 2:
                raise ArgumentError(f"Invalid argument '{entry}'")
            var, value = entry_split
            var = var.strip()
            value = value.strip()
            os.environ[var] = value
            result[var] = value
    return result


def initialize_default_env() -> dict:
    """Set environmental variables from DEFAULT_ENV to their values."""
    result = {}
    for key, value in DEFAULT_ENV.items():
        os.environ[key] = value
        result[key] = value
    return result


class TempEnv:
    """
    Temporarily set values for environmental variables, then restore back previous values.
    !!!NOT THREAD SAFE!!!
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.old_values = None

    def __enter__(self):
        self.old_values = {k: os.getenv(k) for k, _ in self.kwargs.items()}
        for k, v in self.kwargs.items():
            os.environ[k] = v

    def __exit__(self, exc_type, exc_val, exc_tb):
        for k, v in self.old_values.items():
            if v is None:
                del os.environ[k]
            else:
                os.environ[k] = v
