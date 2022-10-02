import logging

from commons.exceptions import CloudFileNotFoundError
from commons.drive_utils.models import download_model_data
from commons.timing import step

LOGGER = logging.getLogger(__name__)

@step
def download_model(model, model_module, **kwargs):
    LOGGER.info(f"Trying to get stored model '{model}'")
    try:
        model_data_path = download_model_data(model)
        LOGGER.info(f"Model data obtained, loading the model using module '{model_module}'")
        model_module.load(model_data_path)
    except CloudFileNotFoundError:
        LOGGER.info(f"Model '{model}' wasn't found on the drive.")