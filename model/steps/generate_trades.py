import logging

LOGGER = logging.getLogger(__name__)


def generate_trades(strategy, strategy_module, y_pred, dataset, **kwargs):
    LOGGER.info(f"Generating trades from strategy '{strategy}'")
    trades = strategy_module.get_trades(y_pred, dataset.get_x())
    return dict(trades=trades)
