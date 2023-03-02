import logging
from core.drive_utils.brokers import download_broker_config

LOGGER = logging.getLogger(__name__)


def initialize_broker(broker, broker_module, broker_config, *args, **kwargs):
    LOGGER.info(f"Getting configuration for '{broker}'")
    if broker_config is None:
        LOGGER.info("No configuration file provided")
        broker_module.initialize()
    else:
        cfg = download_broker_config(broker_config)
        broker_module.initialize(cfg)
