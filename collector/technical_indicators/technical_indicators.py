import sys

import pandas as pd
import pandas_ta as pta
import numpy as np

from commons.dataset import Dataset

def KELCH(df, n):
    KelChM = pd.Series(((df['High'] + df['Low'] + df['Close']) / 3), name='KelChM_' + str(n)).rolling(window=n).mean()
    KelChU = pd.Series(((4 * df['High'] - 2 * df['Low'] + df['Close']) / 3),
                       name='KelChU_' + str(n)).rolling(window=n).mean()
    KelChD = pd.Series(((-2 * df['High'] + 4 * df['Low'] + df['Close']) / 3),
                       name='KelChD_' + str(n)).rolling(window=n).mean()
    df = df.join(KelChM)
    df = df.join(KelChU)
    df = df.join(KelChD)
    return df

def add_sma(df, time_tag, length):
    df[f'SMA_{length}_{time_tag}'] = pta.sma(df["Close"], length=length)

def add_ema(df, time_tag, length):
    df[f'EMA_{length}_{time_tag}'] = pta.ema(df["Close"], length=length)

def add_dema(df, time_tag, length):
    df[f'DEMA_{length}_{time_tag}'] = pta.dema(df["Close"], length=length)

def add_kama(df, time_tag, length):
    df[f'kama_{length}_{time_tag}'] = pta.kama(df["Close"], length=length)

def add_bolinger_bands(df, time_tag):
    bbands_result = pta.bbands(df["Close"], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    df[f'Upperband_{time_tag}'] = bbands_result['BBL_5_2.0']
    df[f'Middleband_{time_tag}'] = bbands_result['BBM_5_2.0']
    df[f'Lowerband_{time_tag}'] = bbands_result['BBU_5_2.0']
    df[f'Bandwidth_{time_tag}'] = bbands_result['BBB_5_2.0']
    df[f'Percent_Column_BBands_{time_tag}'] = bbands_result['BBP_5_2.0']

def add_ichimoku(df, time_tag):
    ichimoku_result = pta.ichimoku(df['High'], df['Low'], df['Close'])
    df[f'Ichimoku_ISA_9_{time_tag}'] = ichimoku_result[0]['ISA_9']
    df[f'Ichimoku_ISB_26_{time_tag}'] = ichimoku_result[0]['ISB_26']
    df[f'Ichimoku_ITS_9_{time_tag}'] = ichimoku_result[0]['ITS_9']
    df[f'Ichimoku_IKS_26_{time_tag}'] = ichimoku_result[0]['IKS_26']

def add_parabolic_sar(df, time_tag):
    PSAR = pta.psar(df['High'], df['Low'])
    df[f'PSAR_PSARl_0.02_0.2_{time_tag}'] = PSAR['PSARl_0.02_0.2']
    df[f'PSARs_0.02_0.2_{time_tag}'] = PSAR['PSARs_0.02_0.2']
    df[f'PSARaf_0.02_0.2_{time_tag}'] = PSAR['PSARaf_0.02_0.2']
    df[f'PSARr_0.02_0.2_{time_tag}'] = PSAR['PSARr_0.02_0.2']

def add_stdev(df, time_tag, length):
    df[f'Standard_deviation_{length}_{time_tag}'] = pta.stdev(df['Close'], length=length)

def add_linreg(df, time_tag, length):
    df[f'Linear_Regression_{length}_{time_tag}'] = pta.linreg(df['Close'], length=length)

def add_atr(df, time_tag, length):
    df[f'Average_True_Range_{length}_{time_tag}'] = pta.atr(df['High'], df['Low'], df['Close'], length=length)

def add_rsi(df, time_tag, length):
    df[f'rsi_{length}_{time_tag}'] = pta.rsi(df['Close'], length=length)

def add_cci(df, time_tag, length):
    df[f'Commodity_Channel_Index_{length}_{time_tag}'] = pta.cci(df['High'], df['Low'], df['Close'], length=length)

def add_momentum(df, time_tag, length):
    df[f'Momentum_{length}_{time_tag}'] = pta.mom(df['Close'], length=length)

def add_macd(df, time_tag):
    macd_result = pta.macd(df['Close'])
    df[f'MACD_12_26_9_{time_tag}'] = macd_result['MACD_12_26_9']
    df[f'MACDh_12_26_9_{time_tag}'] = macd_result['MACDh_12_26_9']
    df[f'MACDs_12_26_9_{time_tag}'] = macd_result['MACDs_12_26_9']

def add_stochrsi(df, time_tag, length=14, rsi_length=14):
    Stoch_RSI = pta.stochrsi(df['Close'], length=length, rsi_length=rsi_length)
    df[f'stoch_rsi_K%_{length}_{time_tag}'] = Stoch_RSI[f'STOCHRSIk_{length}_{rsi_length}_3_3']
    df[f'stoch_rsi_D%_{length}_{time_tag}'] = Stoch_RSI[f'STOCHRSId_{length}_{rsi_length}_3_3']

def add_stoch(df, time_tag):
    Stoch = pta.stoch(df['High'], df['Low'], df['Close'])
    df[f'STOCHk_14_3_3_{time_tag}'] = Stoch['STOCHk_14_3_3']
    df[f'STOCHd_14_3_3_{time_tag}'] = Stoch['STOCHd_14_3_3']

def add_rvi(df, time_tag, length):
    df[f'RVI_{length}_{time_tag}'] = pta.rvi(df['Close'], length=length)

def add_willr(df, time_tag, length):
    df[f'William_R_{length}_{time_tag}'] = pta.willr(df['High'], df['Low'], df['Close'], length=length)

def add_ao(df, time_tag):
    df[f'Awesome_Oscillator_{time_tag}'] = pta.ao(df['High'], df['Low'], )

def add_ha(df, time_tag):
    heikin_result = pta.ha(df['Open'], df['High'], df['Low'], df['Close'])
    df[f'HA_open_{time_tag}'] = heikin_result['HA_open']
    df[f'HA_high_{time_tag}'] = heikin_result['HA_high']
    df[f'HA_low_{time_tag}'] = heikin_result['HA_low']
    df[f'HA_close_{time_tag}'] = heikin_result['HA_close']

def add_donchian(df, time_tag):
    donchian_result = pta.donchian(df['High'], df['Low'])
    df[f'DCL_20_20_{time_tag}'] = donchian_result['DCL_20_20']
    df[f'DCM_20_20_{time_tag}'] = donchian_result['DCM_20_20']
    df[f'DCU_20_20_{time_tag}'] = donchian_result['DCU_20_20']

def add_KELCH(df, time_tag):
    kelch = KELCH(df, 20)
    df[f'KelChM_20_{time_tag}'] = kelch['KelChM_20']
    df[f'KelChU_20_{time_tag}'] = kelch['KelChU_20']
    df[f'KelChD_20_{time_tag}'] = kelch['KelChD_20']

def add_bop(df, time_tag):
    df[f'Balance_of_power_{time_tag}'] = pta.bop(df['Open'], df['High'], df['Low'], df['Close'])

def add_uo(df, time_tag):
    df[f'Ultimate_Oscillator_{time_tag}'] = pta.uo(df['High'], df['Low'], df['Close'])

def add_accbands(df, time_tag):
    acceleration_bands = pta.accbands(df['High'], df['Low'], df['Close'])
    df[f'ACCBL_20_{time_tag}'] = acceleration_bands['ACCBL_20']
    df[f'ACCBM_20_{time_tag}'] = acceleration_bands['ACCBM_20']
    df[f'ACCBU_20_{time_tag}'] = acceleration_bands['ACCBU_20']

def add_cyclical_datetime(df, time_tag):
    timefunc = lambda name, sincos, length: sincos(getattr(df.index, name) / length * 2 * np.pi)
    df[f'Day_sin_{time_tag}'] = timefunc('day', np.sin, 31)
    df[f'Day_cos_{time_tag}'] = timefunc('day', np.cos, 31)
    df[f'Month_sin_{time_tag}'] = timefunc('month', np.sin, 12)
    df[f'Month_cos_{time_tag}'] = timefunc('month', np.cos, 12)
    df[f'Hour_sin_{time_tag}'] = timefunc('hour', np.sin, 24)
    df[f'Hour_cos_{time_tag}'] = timefunc('hour', np.cos, 24)
    df[f'Minute_sin_{time_tag}'] = timefunc('minute', np.sin, 60)
    df[f'Minute_cos_{time_tag}'] = timefunc('minute', np.cos, 60)
    df[f'DayOfWeek_sin_{time_tag}'] = timefunc('dayofweek', np.sin, 7)
    df[f'DayOfWeek_cos_{time_tag}'] = timefunc('dayofweek', np.cos, 7)

def add_us_time(df, time_tag):
    df[f'US_time_{time_tag}'] = np.logical_or(np.logical_and(16 > df.index.hour, df.index.hour >= 10), np.logical_and(df.index.hour == 9, df.index.minute >= 30)).astype(int)

# TODO: add log(df['Open'][t] / df['Open'][t - 1]) etc
def add_log_change(df, time_tag):
    pass

INDICATORS = dict(
    add_sma=[10, 20, 50, 100, 200],
    add_ema=[10, 20, 50, 100, 200],
    add_dema=[10, 20, 50, 100, 200],
    add_kama=[10, 20, 50, 100, 200],
    add_bolinger_bands=None,
    add_ichimoku=None,
    add_parabolic_sar=None,
    add_stdev=[10, 20, 50, 100, 200],
    add_linreg=[10, 20, 50, 100, 200],
    add_atr=[14],
    add_rsi=[14, 26],
    add_cci=[20, 50],
    add_momentum=[10, 14, 21],
    add_macd=None,
    add_stochrsi=[14, [46, 46]],
    add_stoch=None,
    add_rvi=[14],
    add_willr=[14],
    add_ao=None,
    add_ha=None,
    add_donchian=None,
    add_KELCH=None,
    add_bop=None,
    add_uo=None,
    add_accbands=None,
    add_cyclical_datetime=None,
    add_us_time=None,
    add_log_change=None
)

def add_technical_indicators(dataset, time_tag):
    df = dataset.df if isinstance(dataset, Dataset) else dataset
    for indicator, params in INDICATORS.items():
        indicator_func = getattr(sys.modules[__name__], indicator)
        if params is None:
            indicator_func(df, time_tag)
        else:
            for param in params:
                if isinstance(param, list):
                    indicator_func(df, time_tag, *param)
                elif isinstance(param, dict):
                    indicator_func(df, time_tag, **param)
                else:
                    indicator_func(df, time_tag, param)