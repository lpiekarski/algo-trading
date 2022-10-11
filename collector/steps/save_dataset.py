from commons.drive_utils.datasets import upload_dataset
from commons.timing import step
import logging

LOGGER = logging.getLogger(__name__)

@step
def save_dataset(name, df, append, **kwargs):
    if name is None:
        name = df.index[0].strftime("%Y")
        LOGGER.info(f"Dataset name not specified, using current year as the name '{name}'")
    upload_dataset(name, df, append=append)
