import logging

from backtesting import Backtest, Strategy

from commons.timing import step


# back testing 1 add 1 long, 0 do nothing, -1 add 1 short.
# closing on the next time

def get_strategy(kwargs):
    backtest_volume = kwargs['backtest_volume']
    y_pred = kwargs['y_pred']

    class BacktestStrategy(Strategy):
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

    return BacktestStrategy
