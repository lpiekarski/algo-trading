import logging

import commons.dataset as ds
from commons.timing import step

LOGGER = logging.getLogger(__name__)

@step
def get_dataset(dataset=None, *args, **kwargs):
    LOGGER.info("Getting dataset")
    return dict(X=ds.get_dataset(dataset))
