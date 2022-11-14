import logging
from commons.timing import step
from model import predictors, strategies

LOGGER = logging.getLogger(__name__)


@step
def get_strategy_module(strategy, **kwargs):
    strategy_module = strategies.get_strategy_module(strategy)
    return dict(strategies_module=strategy_module)
