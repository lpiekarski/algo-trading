from backtesting import Backtest, Strategy

import warnings
import pandas as pd
import numpy as np
from model.strategies.const_trade_duration import get_strategy

np.seterr(divide='ignore')


def benchmark(dataset, cash, time_tag):
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

    strategy = get_strategy(y_pred, {'backtest_volume': 1})
    bt = Backtest(data,
                  strategy,
                  cash=cash,
                  commission=0,
                  exclusive_orders=True)

    stats = bt.run()
    return stats['Equity Final [$]']


BENCHMARK = ['10y', '1y', '2Q', '1Q', '1m', '1w']


def benchmark_time_tags(df, cash, equity, time_tags=None):
    if time_tags is None:
        time_tags = BENCHMARK

    for params in time_tags:
        if equity < benchmark(df, cash, params):
            return params
            break