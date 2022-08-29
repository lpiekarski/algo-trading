import logging

from commons.timing import run_step

LOGGER = logging.getLogger(__name__)

@run_step
def evaluate_predictions(*args, **kwargs):
    LOGGER.info("Comparing predictions to labels")