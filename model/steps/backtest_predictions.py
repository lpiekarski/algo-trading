import logging

from backtesting import Backtest, Strategy

from commons.timing import step

LOGGER = logging.getLogger(__name__)


@step
def run_backtesting(
        dataset,
        y_pred,
        backtest_threshold,
        backtest_volume,
        backtest_tpsl_pct,
        backtest_commission,
        backtest_leverage,
        backtest_cash,
        strategy_module,
        **kwargs):
    strategy = strategy_module.get_strategy(locals())
    LOGGER.info("Backtesting predictions")

    bt = Backtest(
        dataset.get_x()[['Open', 'High', 'Low', 'Close', 'Volume']],
        strategy,
        commission=backtest_commission,
        margin=(1. / backtest_leverage),
        exclusive_orders=False,
        cash=backtest_cash,
        trade_on_close=True)

    backtest_results = bt.run()
    LOGGER.info(backtest_results)
    bt.plot(resample=False)
    return dict(backtest=bt, backtest_results=backtest_results)
