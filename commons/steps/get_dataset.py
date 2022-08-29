import logging

from commons.dataset import get_dataset
from commons.timing import run_step

LOGGER = logging.getLogger(__name__)

@run_step
def get_dataset(dataset=None, *args, **kwargs):
    LOGGER.info("Getting dataset")
    return dict(X=get_dataset(dataset))
