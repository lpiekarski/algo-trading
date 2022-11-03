import logging

from backtesting import Backtest, Strategy

from commons.timing import step

LOGGER = logging.getLogger(__name__)

@step
def backtest_predictions(dataset, y_pred, backtest_threshold, backtest_volume, backtest_tpsl_pct, backtest_commission, backtest_leverage, backtest_cash, **kwargs):
    LOGGER.info("Backtesting predictions")

    class BacktestStrategy(Strategy):
        def init(self):
            self.id = 1

        def next(self):
            pred = y_pred[self.id]
            close = self.data.Close[-1]
            if pred > 0.5 + backtest_threshold:
                self.buy(size=backtest_volume, tp=close * (1 + backtest_tpsl_pct), sl=close * (1 - backtest_tpsl_pct))
            elif pred < 0.5 - backtest_threshold:
                self.sell(size=backtest_volume, tp=close * (1 - backtest_tpsl_pct), sl=close * (1 + backtest_tpsl_pct))
            self.id += 1

    bt = Backtest(
        dataset.get_x()[['Open', 'High', 'Low', 'Close', 'Volume']],
        BacktestStrategy,
        commission=backtest_commission,
        margin=(1. / backtest_leverage),
        exclusive_orders=False,
        cash=backtest_cash,
        trade_on_close=True)

    backtest_results = bt.run()
    LOGGER.info(backtest_results)
    bt.plot(resample=False)
    return dict(backtest=bt, backtest_results=backtest_results)