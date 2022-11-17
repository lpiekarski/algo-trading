from backtesting import Backtest, Strategy

import warnings
import pandas as pd
import numpy as np


np.seterr(divide='ignore')


def func_benchmark(dataset, cash, time_tag):
    df = dataset.df
    data = df.resample(f'{time_tag}').agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last'})
    data["B"] = data['Open'] <= data['Open'].shift(-1)

    if data.loc[data.index[-1], f'Open'] < data.loc[data.index[-1], f'Close']:
        data.loc[data.index[-1], 'B'] = 1
    else:
        data.loc[data.index[-1], 'B'] = 0

    y_pred = data["B"].shift(0)
    y_pred = pd.concat([y_pred, y_pred.iloc[:1]])
    data = pd.concat([df.iloc[:2], data])

    class benchmark(Strategy):
        def init(self):
            self.id = 0

        def next(self):
            self.position.close()
            pred = y_pred[self.id]
            if pred > 0.5:
                self.buy()
            elif pred < 0.5:
                self.sell()
            self.id += 1

    bt = Backtest(data,
                  benchmark,
                  cash=cash,
                  commission=0,
                  exclusive_orders=True)

    stats = bt.run()
    return stats['Equity Final [$]']


BENCHMARK = ['10y', '1y', '2Q', '1Q', '1m', '1w']


def benchmark(df, cash, equity):
    for params in BENCHMARK:
        if equity < func_benchmark(df, cash, params):
            return params
            break
