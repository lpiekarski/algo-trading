import shutil
import uuid
import os
from functools import wraps


class TempDir:
    def __init__(self, dir_name=None):
        if dir_name is None:
            self.dir_name = os.path.join(os.getenv('TEMP_DIR'), uuid.uuid4().hex)
        else:
            self.dir_name = dir_name

    def __enter__(self):
        os.makedirs(self.dir_name, exist_ok=True)
        return self.dir_name

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self.dir_name, onerror=set_chmod)


def set_chmod(func, path, err):
    os.chmod(path, 0o777)
    func(path)


def inject_tempdir(func):
    """
    Provide a tempdir parameter for the wrapped function - a path to a temporary directory
    which will be removed with all of its content when the wrapped procedure is finished.
    """
    @wraps(func)
    def wrap(*args, **kwargs):
        with TempDir() as td:
            retval = None
            try:
                retval = func(*args, **(kwargs | {"tempdir": td}))
            finally:
                return retval
    return wrap
