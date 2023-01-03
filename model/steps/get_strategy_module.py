import logging
from model import strategies

LOGGER = logging.getLogger(__name__)


def get_strategy_module(strategy, **kwargs):
    strategy_module = strategies.get_strategy_module(strategy)
    return dict(strategy_module=strategy_module)
