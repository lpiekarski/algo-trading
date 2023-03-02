import os

from core.env import require_env, Envfile


def set_var(key, value, **kwargs):
    filename = require_env("DEFAULT_ENV_FILE")
    if os.path.exists(filename):
        envfile = Envfile.parse_from_file(filename)
    else:
        envfile = Envfile([])
    envfile.set_keyword_value(key, value)
    envfile.save(filename)
