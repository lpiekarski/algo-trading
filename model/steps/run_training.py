import logging

from commons.timing import step

LOGGER = logging.getLogger(__name__)

@step
def run_training(model, model_module, dataset, **kwargs):
    LOGGER.info(f"Train model '{model}'")
    model_module.train(dataset.get_X(), dataset.get_y())