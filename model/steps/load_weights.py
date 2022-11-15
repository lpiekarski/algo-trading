import logging
import zipfile

from commons.drive_utils.models import download_model_weights
from commons.exceptions import CloudFileNotFoundError
from commons.tempdir import TempDir
from commons.timing import step

LOGGER = logging.getLogger(__name__)


@step
def load_weights(model, model_module, **kwargs):
    LOGGER.info(f"Trying to get weights for model '{model}'")
    try:
        model_weights_file = download_model_weights(model)
        LOGGER.info(
            f"Model weights obtained, loading the model using module '{model_module}'")
        with TempDir() as td:
            with zipfile.ZipFile(file=model_weights_file, mode='r') as zf:
                zf.extractall(td)
            model_module.load_weights(td)
    except CloudFileNotFoundError:
        LOGGER.info(f"Weights for model '{model}' weren't found.")