import logging

from commons.timing import step

LOGGER = logging.getLogger(__name__)

@step
def run_training(model=None, model_module=None, X=None, y=None, *args, **kwargs):
    LOGGER.info(f"Train model '{model}'")
    model_module.train(X, y)