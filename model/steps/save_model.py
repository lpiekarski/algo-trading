import logging
import os
import zipfile

from commons.drive_utils import get_cache_dir
from commons.drive_utils.models import upload_model_data
from commons.drivepath import clear_cache, from_string
from commons.string import formpath
from commons.tempdir import TempDir
from commons.timing import step

LOGGER = logging.getLogger(__name__)


@step
def save_model(model, model_module, **kwargs):
    model = from_string(model)
    with TempDir() as td1:
        with TempDir() as td2:
            model_data_path = os.path.join(td2, 'model')
            LOGGER.info(
                f"Saving model '{model}' in location: '{formpath(model_data_path)}'")
            model_module.save(td1)
            os.makedirs(os.path.dirname(model_data_path), exist_ok=True)
            with zipfile.ZipFile(file=model_data_path, mode='w') as zf:
                for root, _, files in os.walk(td1):
                    for file in files:
                        path = os.path.join(root, file)
                        zf.write(path, os.path.relpath(path, td1))
            upload_model_data(model_data_path, model)
            clear_cache(model_data_path)
