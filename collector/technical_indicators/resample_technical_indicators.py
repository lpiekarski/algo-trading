import time

import numpy as np
import pandas as pd
import pandas_ta as pta
import bisect

from pandas import DataFrame

from collector.technical_indicators.technical_indicators import *


def add_only_last_sma(df, time_tag, length):
    df_supp = DataFrame(df.tail(length))
    df_supp = add_sma(df_supp, time_tag, length)
    return df_supp


def add_only_last_ema(df, time_tag, length):
    df_supp = DataFrame(df.tail(length))
    df_supp = add_ema(df_supp, time_tag, length)
    return df_supp


def add_only_last_dema(df, time_tag, length):
    df_supp = DataFrame(df.tail(length))
    df_supp = add_dema(df_supp, time_tag, length)
    return df_supp


def add_only_last_kama(df, time_tag, length):
    df_supp = DataFrame(df.tail(length))
    df_supp = add_kama(df_supp, time_tag, length)
    return df_supp


def add_only_last_bolinger_bands(df, time_tag):
    df_supp = DataFrame(df.tail(5))
    df_supp = add_bolinger_bands(df_supp, time_tag)
    return df_supp


def add_only_last_ichimoku(df, time_tag):
    df_supp = DataFrame(df.tail(52))
    df_supp = add_ichimoku(df_supp, time_tag)
    return df_supp


def add_only_last_parabolic_sar(df, time_tag):
    df_supp = DataFrame(df.tail(10))
    df_supp = add_parabolic_sar(df_supp, time_tag)
    return df_supp


def add_only_last_stdev(df, time_tag, length):
    df_supp = DataFrame(df.tail(length))
    df_supp = add_stdev(df_supp, time_tag, length)
    return df_supp


def add_only_last_linreg(df, time_tag, length):
    df_supp = DataFrame(df.tail(length))
    df_supp = add_linreg(df_supp, time_tag, length)
    return df_supp


def add_only_last_atr(df, time_tag, length):
    df_supp = DataFrame(df.tail(length))
    df_supp = add_atr(df_supp, time_tag, length)
    return df_supp


def add_only_last_rsi(df, time_tag, length):
    df_supp = DataFrame(df.tail(length))
    df_supp = add_rsi(df_supp, time_tag, length)
    return df_supp


def add_only_last_cci(df, time_tag, length):
    df_supp = DataFrame(df.tail(length))
    df_supp = add_cci(df_supp, time_tag, length)
    return df_supp


def add_only_last_momentum(df, time_tag, length):
    df_supp = DataFrame(df.tail(length))
    df_supp = add_momentum(df_supp, time_tag, length)
    return df_supp


def add_only_last_macd(df, time_tag):
    df_supp = DataFrame(df.tail(26))
    df_supp = add_macd(df_supp, time_tag)
    return df_supp


def add_only_last_stochrsi(df, time_tag, length=14, rsi_length=14):
    df_supp = DataFrame(df.tail(length))
    df_supp = add_stochrsi(df_supp, time_tag, length, rsi_length)
    return df_supp


def add_only_last_stoch(df, time_tag):
    df_supp = DataFrame(df.tail(14))
    df_supp = add_stoch(df_supp, time_tag)
    return df_supp


def add_only_last_rvi(df, time_tag, length):
    df_supp = DataFrame(df.tail(length))
    df_supp = add_rvi(df_supp, time_tag, length)
    return df_supp


def add_only_last_willr(df, time_tag, length):
    df_supp = DataFrame(df.tail(length))
    df_supp = add_willr(df_supp, time_tag, length)
    return df_supp


def add_only_last_ao(df, time_tag):
    df_supp = DataFrame(df.tail(35))
    df_supp = add_ao(df_supp, time_tag)
    return df_supp


def add_only_last_ha(df, time_tag):
    df_supp = DataFrame(df.tail(10))
    df_supp = add_ha(df_supp, time_tag)
    return df_supp


def add_only_last_donchian(df, time_tag):
    df_supp = DataFrame(df.tail(20))
    df_supp = add_donchian(df_supp, time_tag)
    return df_supp


def add_only_last_KELCH(df, time_tag):
    df_supp = DataFrame(df.tail(10))
    df_supp = add_KELCH(df_supp, time_tag)
    return df_supp


def add_only_last_bop(df, time_tag):
    df_supp = DataFrame(df.tail(10))
    df_supp = add_bop(df_supp, time_tag)
    return df_supp


def add_only_last_uo(df, time_tag):
    df_supp = DataFrame(df.tail(28))
    df_supp = add_uo(df_supp, time_tag)
    return df_supp


def add_only_last_accbands(df, time_tag):
    df_supp = DataFrame(df.tail(10))
    df_supp = add_accbands(df_supp, time_tag)
    return df_supp


def add_only_last_technical_indicators(df, time_tag):
    ### Trend indicators:
    # Moving average
    df = add_only_last_sma(df, time_tag, 10)
    df = add_only_last_sma(df, time_tag, 20)
    df = add_only_last_sma(df, time_tag, 50)
    df = add_only_last_sma(df, time_tag, 100)
    df = add_only_last_sma(df, time_tag, 200)

    # Exponential moving average
    df = add_only_last_ema(df, time_tag, 10)
    df = add_only_last_ema(df, time_tag, 20)
    df = add_only_last_ema(df, time_tag, 50)
    df = add_only_last_ema(df, time_tag, 100)
    df = add_only_last_ema(df, time_tag, 200)

    # Double Exponential moving average
    df = add_only_last_dema(df, time_tag, 10)
    df = add_only_last_dema(df, time_tag, 20)
    df = add_only_last_dema(df, time_tag, 50)
    df = add_only_last_dema(df, time_tag, 100)
    df = add_only_last_dema(df, time_tag, 200)

    # Kaufman's Adaptive Moving Average
    df = add_only_last_kama(df, time_tag, 10)
    df = add_only_last_kama(df, time_tag, 20)
    df = add_only_last_kama(df, time_tag, 50)
    df = add_only_last_kama(df, time_tag, 100)
    df = add_only_last_kama(df, time_tag, 200)

    # Bolinger Bands
    df = add_only_last_bolinger_bands(df, time_tag)

    # Ichimoku
    # df = add_only_last_ichimoku(df, time_tag)

    # Parabolic SAR
    df = add_only_last_parabolic_sar(df, time_tag)

    # Standard deviation
    df = add_only_last_stdev(df, time_tag, 10)
    df = add_only_last_stdev(df, time_tag, 20)
    df = add_only_last_stdev(df, time_tag, 50)
    df = add_only_last_stdev(df, time_tag, 100)
    df = add_only_last_stdev(df, time_tag, 200)

    # Regression
    df = add_only_last_linreg(df, time_tag, 10)
    df = add_only_last_linreg(df, time_tag, 20)
    df = add_only_last_linreg(df, time_tag, 50)
    df = add_only_last_linreg(df, time_tag, 100)
    df = add_only_last_linreg(df, time_tag, 200)

    # more?
    ###Oscillators:
    # Average True Range
    df = add_only_last_atr(df, time_tag, 14)

    # RSI 14
    df = add_only_last_rsi(df, time_tag, 14)
    df = add_only_last_rsi(df, time_tag, 26)

    # Commodity Channel Index
    df = add_only_last_cci(df, time_tag, 20)
    df = add_only_last_cci(df, time_tag, 50)

    # Momentum
    df = add_only_last_momentum(df, time_tag, 10)
    df = add_only_last_momentum(df, time_tag, 14)
    df = add_only_last_momentum(df, time_tag, 21)

    # MACD
    # df = add_only_last_macd(df, time_tag)

    # Stochastic RSI
    # df = add_only_last_stochrsi(df, time_tag, 14)
    # df = add_only_last_stochrsi(df, time_tag, length=46, rsi_length=46)

    # Stochastic
    # df = add_only_last_stoch(df, time_tag)

    # Relative Vigor Index
    df = add_only_last_rvi(df, time_tag, 14)

    # R Williams
    df = add_only_last_willr(df, time_tag, 14)

    ###Volumes ?
    ### others: (mainly mixes of both)
    # Awesome Oscillator
    df = add_only_last_ao(df, time_tag)

    # Heikin Ashi
    df = add_only_last_ha(df, time_tag)

    # Donchian Channel
    # df = add_only_last_donchian(df, time_tag)

    # Keltner Channel
    df = add_only_last_KELCH(df, time_tag)

    # Balance of power
    df = add_only_last_bop(df, time_tag)

    # Ultimate oscillator
    df = add_only_last_uo(df, time_tag)

    # Acceleration Bands
    # df = add_only_last_accbands(df, time_tag)

    return df


def resample_technical_indicators(df, time_tag="1h"):
    ohlc = {
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last'
    }
    result_df = []
    # Loop on each minutes
    actual_time = None
    resample_df = None
    size = len(df.index)
    count = 0
    for index, row in df.iterrows():
        count += 1
        if actual_time != index.round(time_tag):
            # da się zapamiętać ostatnie.
            actual_time = index.round(time_tag)
            past_supp_df = df.loc[df.index < actual_time]
            # resample past records
            past_resample_df = past_supp_df.resample(time_tag).apply(ohlc)
        # resample actual sample
        mask = (df.index >= actual_time) & (df.index <= index)
        supp_df = df.loc[mask]
        resample_df = supp_df.resample(time_tag).apply(ohlc)
        resample_df = pd.concat([past_resample_df, resample_df])

        if len(resample_df.index) < 200:
            continue
        resample_df = resample_df.tail(200)
        resample_df = add_only_last_technical_indicators(resample_df, time_tag)

        last_record = resample_df.iloc[-1]
        last_record.name = index

        result_df.append(last_record)

        progress_bar = count / size
        if count % 500 == 0 or count == size:
            print(f"{count}/{size} = {100 * progress_bar}%")
            print("----")
    return DataFrame(result_df)


if __name__ == '__main__':
    df = pd.read_csv('M1_test.csv', index_col=0, dayfirst=True, parse_dates=True)
    print(df)
    ohlc = {
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last'
    }
    resample_df = df.resample("30min").apply(ohlc)  # 5min #30min #1h #1d #1w #1m

    print(resample_df)
    # resample_df.to_csv('30M.csv')
    df_ind = resample_technical_indicators(resample_df, time_tag="1h")
    resample_df = pd.concat([resample_df, df_ind], axis=1, join='inner')
    print(resample_df)