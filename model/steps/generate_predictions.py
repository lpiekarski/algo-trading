import logging

LOGGER = logging.getLogger(__name__)


def generate_predictions(model, model_module, dataset, **kwargs):
    LOGGER.info(f"Generating predictions from model '{model}'")
    y_pred = model_module.predict(dataset.get_x())
    return dict(y_pred=y_pred)
