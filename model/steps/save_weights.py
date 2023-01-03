import logging
import os
import zipfile

from commons.drive_utils.models import upload_model_weights
from commons.drivepath import clear_cache, from_string
from commons.string import formpath
from commons.tempdir import TempDir

LOGGER = logging.getLogger(__name__)


def save_weights(model, model_module, **kwargs):
    model = from_string(model)
    with TempDir() as td1:
        with TempDir() as td2:
            model_data_path = os.path.join(td2, 'model')
            LOGGER.info(
                f"Saving weights for '{model}' in location: '{formpath(model_data_path)}'")
            model_module.save_weights(td1)
            os.makedirs(os.path.dirname(model_data_path), exist_ok=True)
            with zipfile.ZipFile(file=model_data_path, mode='w') as zf:
                for root, _, files in os.walk(td1):
                    for file in files:
                        path = os.path.join(root, file)
                        zf.write(path, os.path.relpath(path, td1))
            upload_model_weights(model_data_path, model)
            clear_cache(model_data_path)
