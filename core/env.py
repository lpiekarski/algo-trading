import os
from typing import List, Dict

from core.exceptions import ArgumentError

__all__ = ["require_env", "set_env_from_file", "initialize_default_env", "TempEnv"]

DEFAULT_ENV = dict(
    CACHE_DIR="./.cache",
    TEMP_DIR="./.tmp",
    drive="local",
    GIT_DRIVE_MAX_FILE_SIZE="100000000",
    DEFAULT_ENV_FILE=os.path.join(os.path.expanduser("~"), ".atf")
)


def require_env(name: str) -> str:
    """Get environmental variable with given name. Raise "ArgumentError" if the variable has no value set."""
    value = os.getenv(name)
    if value is None:
        raise ArgumentError(f"Missing environment variable '{name}'")
    return value


class EnvfileDirective:
    def __init__(self):
        pass


class ImportDirective(EnvfileDirective):
    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename

    def __str__(self):
        return f"import {self.filename}"


class CommentDirective(EnvfileDirective):
    def __init__(self, content: str):
        super().__init__()
        self.content = content

    def __str__(self):
        return f"#{self.content}"


class KeywordValueDirective(EnvfileDirective):
    def __init__(self, keyword: str, value: str):
        super().__init__()
        self.keyword = keyword
        self.value = value

    def __str__(self):
        return f"{self.keyword}={self.value}"


class Envfile:
    def __init__(self, directives: List[EnvfileDirective]):
        self.directives = directives

    @classmethod
    def parse_from_file(cls, filename: str) -> "Envfile":
        result = []
        with open(filename, "r") as f: #czy to nie bierze z absolutnej ścieki? Nie lepiej z relatywnej? 
            lines = f.readlines()
            lines = list(filter(lambda line: line != "", lines))
            lines = list(filter(lambda line: not line.isspace(), lines))
            for directive in lines:
                directive = directive.lstrip()
                if directive.startswith("import "):
                    imported_file = directive.split(" ", 1)[1].strip()
                    result.append(ImportDirective(imported_file))
                elif directive.startswith("#"):
                    content = directive[1:] if len(directive) > 1 else ""
                    result.append(CommentDirective(content))
                else:
                    entry_split = directive.split("=", 1)
                    if len(entry_split) != 2:
                        raise ArgumentError(f"Invalid argument '{directive}'")
                    var, value = entry_split
                    var = var.strip()
                    value = value.strip()
                    result.append(KeywordValueDirective(var, value))
        return Envfile(result)

    def execute(self) -> Dict[str, str]:
        result = {}
        for directive in self.directives:
            if isinstance(directive, ImportDirective):
                result |= Envfile.parse_from_file(directive.filename).execute()
            elif isinstance(directive, KeywordValueDirective):
                os.environ[directive.keyword] = directive.value
                result[directive.keyword] = directive.value
        return result

    def save(self, filename: str) -> None:
        with open(filename, "w") as f:
            f.writelines([str(directive) + "\n" for directive in self.directives])

    def set_keyword_value(self, keyword: str, value: str):
        self.unset_keyword(keyword)
        self.directives.append(KeywordValueDirective(keyword, value))

    def unset_keyword(self, keyword: str):
        self.directives = [
            directive
            for directive in self.directives
            if not isinstance(directive, KeywordValueDirective) or directive.keyword != keyword
        ]


def set_env_from_file(filename: str) -> dict:
    """
    Read env file consisting of "var_name=value" lines. Store environmental variables present in that file
    directly to os.environ.

    Returns a dictionary of all variables read from the file
    """
    return Envfile.parse_from_file(filename).execute()


def initialize_default_env() -> dict:
    """Set environmental variables from DEFAULT_ENV to their values."""
    result = {}
    for key, value in DEFAULT_ENV.items():
        os.environ[key] = value
        result[key] = value
    envfile = os.getenv("DEFAULT_ENV_FILE")
    if os.path.exists(envfile):
        set_env_from_file(envfile)
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
