import json
import logging

from backtesting import Backtest

from commons.drivepath import cache

LOGGER = logging.getLogger(__name__)


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
        with open(file, 'r') as f:
            cfg = json.load(f)
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
