import logging

from commons.timing import run_step
from model.predictors import get_model_module

LOGGER = logging.getLogger(__name__)

@run_step
def run_training(model=None, X=None, y=None, *args, **kwargs):
    LOGGER.info(f"Train model '{model}'")
    model_module = get_model_module(model)
    model_module.train(X, y)