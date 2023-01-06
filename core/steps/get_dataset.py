import datetime
import logging

import core.drive_utils.datasets as ds

LOGGER = logging.getLogger(__name__)


def get_dataset(dataset, **kwargs):
    LOGGER.info("Getting dataset")
    if dataset is None:
        dataset = str(datetime.datetime.now().year)
        LOGGER.info(
            f"Dataset not specified, using current year dataset '{dataset}'")
    return dict(dataset_name=dataset, dataset=ds.download_dataset(dataset))
