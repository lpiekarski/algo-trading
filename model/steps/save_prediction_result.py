import datetime
import logging
from commons.drive_utils.predictions import upload_prediction
from commons.timing import step
import pandas as pd

LOGGER = logging.getLogger(__name__)

@step
def save_prediction_result(output, model, dataset, y_pred, **kwargs):
    if output is None:
        time = datetime.datetime.now()
        output = f"prediction_{model}_{time.year}_{time.month}_{time.day}_{time.hour}_{time.minute}"
    LOGGER.info(f"Saving results as '{output}'")
    upload_prediction(output, pd.DataFrame(y_pred))
