import json
import logging
import pandas as pd

from backtesting import Backtest, Strategy

from commons.drivepath import cache
from commons.timing import step
from commons.validation.cagr import cagr_ratio
from commons.validation.benchmark import benchmark
from commons.data.utils import log_change

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
    benchmark_lvl = benchmark(dataset,
                              starting_cash,
                              backtest_results['Equity Final [$]'])
    cagr = cagr_ratio(starting_cash,
                      backtest_results['Equity Final [$]'],
                      backtest_results['Duration'].days / 365.25)
    backtest_results = pd.DataFrame(backtest_results)
    #backtest_results["CAGR Ratio"] = cagr
    #backtest_results["Benchmark"] = benchmark_lvl
    LOGGER.info(backtest_results)
    bt.plot(resample=False)
    return dict(backtest=bt, backtest_results=backtest_results)
