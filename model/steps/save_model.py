import logging
import os
import zipfile

from commons.drive_utils.models import get_model_cache_path, upload_model_data
from commons.string import formpath
from commons.tempdir import TempDir
from commons.timing import step

LOGGER = logging.getLogger(__name__)

@step
def save_model(model, model_module, **kwargs):
    model_data_path = get_model_cache_path(model)
    LOGGER.info(f"Saving model '{model}' in location: '{formpath(model_data_path)}'")
    with TempDir() as td:
        model_module.save(td)
        with zipfile.ZipFile(file=model_data_path, mode='w') as zf:
            for root, _, files in os.walk(td):
                for file in files:
                    path = os.path.join(root, file)
                    zf.write(path, os.path.relpath(path, td))
    upload_model_data(model)
