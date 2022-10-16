import logging

import collector.technical_indicators.labels as ls
from commons.timing import step

LOGGER = logging.getLogger(__name__)

@step
def add_labels(dataset, **kwargs):
    ls.add_labels(dataset)
