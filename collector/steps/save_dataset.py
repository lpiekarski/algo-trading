from core.data.dataset import Dataset
from core.drive_utils.datasets import upload_dataset
import logging

LOGGER = logging.getLogger(__name__)


def save_dataset(output, dataset: Dataset, append, **kwargs):
    if output is None:
        output = dataset.df.index[0].strftime("%Y")
        LOGGER.info(
            f"Dataset name not specified, using current year as the name '{output}'")
    upload_dataset(output, dataset, append=append)
