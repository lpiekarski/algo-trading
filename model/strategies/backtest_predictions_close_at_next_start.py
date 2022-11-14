import logging

from backtesting import Backtest, Strategy

from commons.timing import step

LOGGER = logging.getLogger(__name__)

# back testing 1 add 1 long, 0 do nothing, -1 add 1 short.
# closing on the next time


@step
def backtest_predictions_close_at_next_start(
    dataset,
    y_pred,
    backtest_volume,
    backtest_commission,
    backtest_leverage,
    backtest_cash,
    **kwargs):
    LOGGER.info("Backtesting predictions")


    class BacktestStrategy_v2(Strategy):
        def init(self):
            self.id = 1

        def next(self):
            pred = y_pred[self.id]
            close = self.data.Close[-1]
            self.position.close()
            if pred > 0.5:
                self.buy(size=backtest_volume)
            elif pred < -0.5:
                self.sell(size=backtest_volume)
            self.id += 1

    bt = Backtest(
        dataset.get_x()[['Open', 'High', 'Low', 'Close', 'Volume']],
        BacktestStrategy_v2,
        commission=backtest_commission,
        margin=(1. / backtest_leverage),
        exclusive_orders=False,
        cash=backtest_cash,
        trade_on_close=True)

    backtest_results = bt.run()
    LOGGER.info(backtest_results)
    bt.plot(resample=False)
    return dict(backtest=bt, backtest_results=backtest_results)