import os

from core.env import require_env, Envfile


def unset_var(key, **kwargs):
    filename = require_env("DEFAULT_ENV_FILE")
    if os.path.exists(filename):
        envfile = Envfile.parse_from_file(filename)
    else:
        envfile = Envfile([])
    envfile.unset_keyword(key)
    envfile.save(filename)
