import logging

from collector.technical_indicators.labels import add_best_decision
from commons.timing import step

LOGGER = logging.getLogger(__name__)

@step
def add_labels(dataset, deviation, **kwargs):
    add_best_decision(dataset, deviation)
