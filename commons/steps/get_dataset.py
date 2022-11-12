import datetime
import logging

import commons.drive_utils.datasets as ds
from commons.timing import step

LOGGER = logging.getLogger(__name__)


@step
def get_dataset(dataset, **kwargs):
    LOGGER.info("Getting dataset")
    if dataset is None:
        dataset = str(datetime.datetime.now().year)
        LOGGER.info(
            f"Dataset not specified, using current year dataset '{dataset}'")
    return dict(dataset_name=dataset, dataset=ds.download_dataset(dataset))
