from commons.dataset import Dataset
from commons.drive_utils.datasets import upload_dataset
from commons.timing import step
import logging

LOGGER = logging.getLogger(__name__)

@step
def save_dataset(name, dataset: Dataset, append, **kwargs):
    if name is None:
        name = dataset.df.index[0].strftime("%Y")
        LOGGER.info(f"Dataset name not specified, using current year as the name '{name}'")
    upload_dataset(name, dataset, append=append)
