import logging

LOGGER = logging.getLogger(__name__)


def generate_predictions(model, model_module, dataset, label, **kwargs):
    LOGGER.info(f"Generating predictions from model '{model}'")
    if label is None and len(dataset.labels) == 1:
        LOGGER.info(f"Dataset implied label '{dataset.labels[0]}'")
        label = dataset.labels[0]
    src = dataset.get_x()
    tgt = dataset.get_y(*label.split(","))
    LOGGER.debug(f"Generating predictions from data: {src}, labels: {tgt}")
    LOGGER.info(f"Generating predictions for {src.shape[0]} observations")
    y_pred = model_module.predict(src, tgt)
    LOGGER.debug(f"Predictions: {y_pred}")
    return dict(y_pred=y_pred)
