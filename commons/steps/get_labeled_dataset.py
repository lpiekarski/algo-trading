import logging

from commons.drive_utils.datasets import download_dataset
from commons.exceptions import CloudFileNotFoundError
from commons.timing import step

LOGGER = logging.getLogger(__name__)

@step
def get_labeled_dataset(dataset, label, **kwargs):
    LOGGER.info(f"Getting labeled dataset '{dataset}'")
    try:
        X = download_dataset(dataset)
        y = X[label].copy()
        X.drop(label, axis=1, inplace=True)
        X.drop(list(X.filter(regex=r'^next_long_.*$')), axis=1, inplace=True)
        X.drop(list(X.filter(regex=r'^next_short_.*$')), axis=1, inplace=True)
        X.drop(list(X.filter(regex=r'^Long_short_.*$')), axis=1, inplace=True)
    except CloudFileNotFoundError as e:
        LOGGER.error(f"Cannot find dataset '{dataset}'")
        raise e
    return dict(X=X, y=y)