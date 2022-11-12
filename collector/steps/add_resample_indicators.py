import logging

from collector.technical_indicators.resample_technical_indicators import resample_technical_indicators
from commons.timing import step

LOGGER = logging.getLogger(__name__)


@step
def add_resample_indicators(dataset, time_tag, *args, **kwargs):
    LOGGER.info(f"reshape to time unit '{time_tag}'")
    dataset.concat(resample_technical_indicators(
        dataset, time_tag=time_tag), axis=1, join='inner')
