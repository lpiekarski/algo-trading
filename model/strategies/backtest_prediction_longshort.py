import logging

from backtesting import Backtest, Strategy

from commons.timing import step


class BacktestStrategy(Strategy):
    def init(self):
        self.id = 1

    def next(self):
        pred = y_pred[self.id]
        close = self.data.Close[-1]
        if pred > 0.5 + backtest_threshold:
            self.buy(size=backtest_volume,
                     tp=close * (1 + backtest_tpsl_pct),
                     sl=close * (1 - backtest_tpsl_pct))
        elif pred < 0.5 - backtest_threshold:
            self.sell(size=backtest_volume,
                      tp=close * (1 - backtest_tpsl_pct),
                      sl=close * (1 + backtest_tpsl_pct))
        self.id += 1