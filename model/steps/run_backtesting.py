import json
import logging

from backtesting import Backtest, Strategy

from commons.drivepath import cache
from commons.timing import step

LOGGER = logging.getLogger(__name__)


@step
def run_backtesting(
        dataset,
        y_pred,
        commission,
        leverage,
        starting_cash,
        strategy_module,
        strategy_config,
        **kwargs):
    if strategy_config is not None:
        file, _ = cache(strategy_config)
        cfg = json.load(file)
    else:
        cfg = None
    strategy = strategy_module.get_strategy(y_pred, cfg)
    LOGGER.info("Backtesting predictions")

    bt = Backtest(
        dataset.get_x(),
        strategy,
        commission=commission,
        margin=(1. / leverage),
        exclusive_orders=False,
        cash=starting_cash,
        trade_on_close=True)

    backtest_results = bt.run()
    LOGGER.info(backtest_results)
    bt.plot(resample=False)
    return dict(backtest=bt, backtest_results=backtest_results)
