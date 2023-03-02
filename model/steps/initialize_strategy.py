import logging
from core.drive_utils.strategies import download_strategy_config

LOGGER = logging.getLogger(__name__)


def initialize_strategy(strategy, strategy_module, strategy_config, **kwargs):
    LOGGER.info(f"Getting configuration for '{strategy}'")
    if strategy_config is None:
        LOGGER.info("No configuration file provided")
        strategy_module.initialize()
    else:
        cfg = download_strategy_config(strategy_config)
        strategy_module.initialize(cfg)
