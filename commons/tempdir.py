import shutil
import uuid
import os

from commons.env import getenv

class TempDir:
    def __init__(self):
        self.dir_name = os.path.join(getenv('TEMP_DIR'), uuid.uuid4().hex)

    def __enter__(self):
        os.makedirs(self.dir_name, exist_ok=True)
        return self.dir_name

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self.dir_name, onerror=set_chmod)

def set_chmod(func, path, err):
    os.chmod(path, 0o777)
    func(path)