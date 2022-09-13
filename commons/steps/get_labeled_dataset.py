import logging

from commons.drive_utils.datasets import download_dataset
from commons.exceptions import CloudFileNotFoundError
from commons.timing import step

LOGGER = logging.getLogger(__name__)

@step
def get_labeled_dataset(dataset=None, *args, **kwargs):
    LOGGER.info(f"Getting labeled dataset '{dataset}'")
    try:
        X = download_dataset(dataset)
        y = X["y"].copy()
        X.drop('y', axis=1, inplace=True)
    except CloudFileNotFoundError as e:
        LOGGER.error(f"Cannot find dataset '{dataset}'")
        raise e
    return dict(X=X, y=y)