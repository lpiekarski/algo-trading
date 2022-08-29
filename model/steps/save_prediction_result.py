import logging

from commons.dataset import put_dataset
from commons.timing import run_step

LOGGER = logging.getLogger(__name__)

@run_step
def save_prediction_result(output=None, model=None, dataset=None, y_pred=None, *args, **kwargs):
    if output is None:
        output = f"{dataset}_results_{model}"
    LOGGER.info(f"Saving results as '{output}'")
    put_dataset(output, y_pred)
