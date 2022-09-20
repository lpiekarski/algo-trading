import logging
import os

from commons.drive_utils.models import get_model_cache_path, upload_model_data
from commons.exceptions import BotError
from commons.timing import step

LOGGER = logging.getLogger(__name__)

@step
def save_model(skip_save=None, model=None, model_module=None, *args, **kwargs):
    if skip_save:
        LOGGER.info(f"Skipping saving the model.")
        return
    model_data_path = get_model_cache_path(model)
    try:
        os.remove(model_data_path)
    except FileNotFoundError:
        pass
    except Exception as e:
        raise BotError('Error when trying to remove model data', e)
    model_module.save(model_data_path)
    LOGGER.info(f"Saving model '{model}' in location: '{model_data_path}'")
    upload_model_data(model)
