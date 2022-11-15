import logging

from commons.drive_utils.models import download_model_config
from commons.timing import step

LOGGER = logging.getLogger(__name__)


@step
def initialize_model(model, model_module, model_config, dataset, **kwargs):
    LOGGER.info(f"Getting configuration for '{model}'")
    if model_config is None:
        LOGGER.info("No configuration file provided")
        model_module.initialize(dataset.num_features(), None)
    else:
        cfg = download_model_config(model_config)
        model_module.initialize(dataset.num_features(), cfg)
