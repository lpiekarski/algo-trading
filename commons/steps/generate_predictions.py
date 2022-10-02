import logging

from commons.timing import step

LOGGER = logging.getLogger(__name__)

@step
def generate_predictions(model, model_module, X, **kwargs):
    LOGGER.info(f"Generating predictions from model '{model}'")
    y_pred = model_module.predict(X)
    return dict(y_pred=y_pred)