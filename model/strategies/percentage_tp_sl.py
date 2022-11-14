from backtesting import Strategy


def get_strategy(kwargs):
    y_pred = kwargs['y_pred']
    backtest_threshold = kwargs['backtest_threshold']
    backtest_volume = kwargs['backtest_volume']
    backtest_tpsl_pct = kwargs['backtest_tpsl_pct']

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

    return BacktestStrategy
