import logging

from commons.timing import step

LOGGER = logging.getLogger(__name__)

@step
def run_training(model, model_module, dataset, label, **kwargs):
    LOGGER.info(f"Train model '{model}'")
    if label is None and len(dataset.labels) == 1:
        LOGGER.info(f"Dataset implied label '{dataset.labels[0]}'")
        label = dataset.labels[0]
    model_module.train(dataset.get_x(), dataset.get_y(label))