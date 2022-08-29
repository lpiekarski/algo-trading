import logging

from commons.timing import step
from model.predictors import get_model_module

LOGGER = logging.getLogger(__name__)

@step
def generate_predictions(model=None, X=None, *args, **kwargs):
    LOGGER.info("Generating predictions from model")
    model_module = get_model_module(model)
    y_pred = model_module.predict(X)
    return dict(y_pred=y_pred)