import datetime
import logging
from commons.drive_utils.predictions import upload_prediction
import pandas as pd

LOGGER = logging.getLogger(__name__)


def save_prediction_result(output, model, dataset_name, y_pred, **kwargs):
    if output is None:
        time = datetime.datetime.now()
        dataset_name = dataset_name.replace('/', '_').replace(':', '_')
        output = f"prediction_{dataset_name}_{model}_{time.year:04}{time.month:02}{time.day:02}{time.hour:02}{time.minute:02}"
    LOGGER.info(f"Saving results as '{output}'")
    upload_prediction(output, pd.DataFrame(y_pred))
