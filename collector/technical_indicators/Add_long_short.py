
import numpy as np
import pandas as pd
import bisect

def find_next_time_with_diff_price(df, x, direction):
    df['Open'] *= direction
    df['Low'] *= direction
    stack = []
    next_long = np.full(len(df), np.nan)
    ohlc = {
        'Open': 'first',
        'time': 'first'
    }
    df_year = df.resample('1y').apply(ohlc)  # 5min #30min #1h #1d #1w #1m
    df_year_multiply = df_year.copy()
    df_year_multiply['Open'] = df_year_multiply['Open'] * x * direction
    if direction == 1:
        for i in range(len(df)):
            year = df.iloc[i].time.year
            while stack and df['High'].iloc[i] > stack[0][1]:
                stack_time_index, stack_price = stack.pop(0)
                next_long[stack_time_index] = i
            year_val = df_year_multiply[df_year_multiply['time'].dt.year == year]
            val = df['Open'].iloc[i] + year_val['Open'].iloc[0]
            stack.insert(bisect.bisect(stack, val, key=lambda e: e[1]), (i, val))
    else:
        for i in range(len(df)):
            year = df.iloc[i].time.year
            while stack and df['Low'].iloc[i] > stack[0][1]:
                stack_time_index, stack_price = stack.pop(0)
                next_long[stack_time_index] = i
            year_val = df_year_multiply[df_year_multiply['time'].dt.year == year]
            val = df['Open'].iloc[i] + year_val['Open'].iloc[0]
            stack.insert(bisect.bisect(stack, val, key=lambda e: e[1]), (i, val))

    df['Open'] *= direction
    df['Low'] *= direction
    return next_long

def add_long_short(df, x):
    df[f'next_long_{x}'] = find_next_time_with_diff_price(df, x, direction=1)
    df[f'next_short_{x}'] = find_next_time_with_diff_price(df, x, direction=-1)

    df[f'next_long_{x}'] = df[f'next_long_{x}'].replace(np.nan, 99999999)
    df[f'next_short_{x}'] = df[f'next_short_{x}'].replace(np.nan, 99999999)

    df[f'Long_short_{x}'] = df.apply(lambda y: '1' if y[f'next_long_{x}'] <=
                                                       y[f'next_short_{x}'] else 0, axis=1)
    return df

if __name__ == '__main__':
    df = pd.read_csv('M1.csv', index_col=0, parse_dates=True)

    df['time'] = pd.to_datetime(df.index)

    print(
        f'{len(df):,.0f} rows with {len(df["Open"].unique()):,.0f} unique prices ranging from ${df["Open"].min():,.2f} to ${df["Open"].max():,.2f}')

    # 0.01
    add_long_short(df, 0.01)

    # 0.025
    add_long_short(df, 0.025)

    # 0.05
    add_long_short(df, 0.05)

    print(df)