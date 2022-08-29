import logging

from commons.timing import step

LOGGER = logging.getLogger(__name__)

@step
def evaluate_predictions(*args, **kwargs):
    LOGGER.info("Comparing predictions to labels")