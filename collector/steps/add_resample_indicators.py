import logging

from commons.timing import step

LOGGER = logging.getLogger(__name__)


@step
def add_resample_indicators(dataset, time_tag, *args, **kwargs):
    raise NotImplementedError("TODO: https://github.com/lpiekarski/algo-trading/issues/126")
