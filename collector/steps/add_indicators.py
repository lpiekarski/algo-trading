import logging

from collector.technical_indicators.technical_indicators import add_technical_indicators
from commons.timing import step

LOGGER = logging.getLogger(__name__)


@step
def add_indicators(dataset, **kwargs):
    dataset.df = add_technical_indicators(
        dataset, time_tag=f"{dataset.interval.total_seconds():.0f}s")
