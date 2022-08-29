import logging

from commons.dataset import get_dataset
from commons.exceptions import CloudFileNotFoundError
from commons.timing import step

LOGGER = logging.getLogger(__name__)

@step
def get_train_dataset(dataset=None, *args, **kwargs):
    LOGGER.info(f"Getting dataset '{dataset}'")
    try:
        X = get_dataset(dataset)
        y = X["y"].copy()
        X.drop('y', axis=1, inplace=True)
    except CloudFileNotFoundError as e:
        LOGGER.error(f"Cannot find dataset '{dataset}'")
        raise e
    return dict(X=X, y=y)