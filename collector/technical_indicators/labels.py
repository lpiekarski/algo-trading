import numpy as np
import pandas as pd
import bisect

from commons.dataset import Dataset

def add_best_decision(dataset: Dataset, deviation):
    next_long = np.nan_to_num(find_next_time_with_diff_price(dataset.df, deviation, direction=1), nan=np.inf)
    next_short = np.nan_to_num(find_next_time_with_diff_price(dataset.df, deviation, direction=-1), nan=np.inf)
    dataset.add_label(f'Best_decision_{deviation}', np.argmax(np.concatenate([np.expand_dims(next_short, 1), np.expand_dims(next_long, 1)], axis=1), axis=1))

def find_next_time_with_diff_price(df_: pd.DataFrame, deviation, direction):
    df = df_.copy()
    df['Close'] *= direction
    df['Low'] *= direction
    stack = []
    next_long = np.full(len(df), np.nan)
    ohlc = {
        'Open': 'first',
        'time': 'first'
    }
    df_year = df.resample('1y').apply(ohlc)  # 5min #30min #1h #1d #1w #1m
    df_year_multiply = df_year.copy()
    df_year_multiply['Open'] = df_year_multiply['Open'] * deviation * direction  #TODO: assumes that df contains the  first 'Open' of the year, this is not correct
    col = 'High' if direction == 1 else 'Low'
    for i in range(len(df)):
        year = df.iloc[i].name.year
        while stack and df[col].iloc[i] > stack[0][1]:
            stack_time_index, stack_price = stack.pop(0)
            next_long[stack_time_index] = i
        year_val = df_year_multiply[df_year_multiply.index.year == year]
        val = df['Close'].iloc[i] + direction * year_val['Open'].iloc[0]
        _, snd = zip(*stack) if stack else ([], [])
        idx = bisect.bisect(snd, val)
        stack.insert(idx, (i, val))

    return next_long