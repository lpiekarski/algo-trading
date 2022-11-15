from typing import Type, Any

import numpy as np
from backtesting import Strategy


def get_strategy(predictions: np.ndarray, config_json: Any) -> Type[Strategy]:
    backtest_threshold = config_json['backtest_threshold']
    backtest_volume = config_json['backtest_volume']
    backtest_tpsl_pct = config_json['backtest_tpsl_pct']

    class BacktestStrategy(Strategy):
        def init(self):
            self.id = 1

        def next(self):
            pred = predictions[self.id]
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
