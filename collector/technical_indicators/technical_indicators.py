import sys

import pandas as pd
import pandas_ta as pta
import numpy as np
from tqdm import tqdm

from commons.data.dataset import Dataset
from commons.data.utils import log_change


def sma(df, time_tag, length):
    return [pd.Series(
        name=f'SMA_log_change_{length}_{time_tag}',
        data=log_change(pta.sma(df["Close"], length=length))
    )]


def ema(df, time_tag, length):
    return [pd.Series(
        name=f'EMA_log_change_{length}_{time_tag}',
        data=log_change(pta.ema(df["Close"], length=length))
    )]


def dema(df, time_tag, length):
    return [pd.Series(
        name=f'DEMA_{length}_{time_tag}',
        data=log_change(pta.dema(df["Close"], length=length))
    )]


def kama(df, time_tag, length):
    return [pd.Series(
        name=f'kama_{length}_{time_tag}',
        data=log_change(pta.kama(df["Close"], length=length))
    )]


def bolinger_bands(df, time_tag):
    bbands_result = pta.bbands(
        df["Close"], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    return [
        pd.Series(
            name=f'Upperband_{time_tag}',
            data=bbands_result['BBL_5_2.0']
        ),
        pd.Series(
            name=f'Middleband_{time_tag}',
            data=bbands_result['BBM_5_2.0']
        ),
        pd.Series(
            name=f'Lowerband_{time_tag}',
            data=bbands_result['BBU_5_2.0']
        ),
        pd.Series(
            name=f'Bandwidth_{time_tag}',
            data=bbands_result['BBB_5_2.0']
        ),
        pd.Series(
            name=f'Percent_Column_BBands_{time_tag}',
            data=bbands_result['BBP_5_2.0']
        )
    ]


def ichimoku(df, time_tag):
    ichimoku_result = pta.ichimoku(df['High'], df['Low'], df['Close'])
    return [
        pd.Series(
            name=f'Ichimoku_ISA_9_{time_tag}',
            data=ichimoku_result[0]['ISA_9']
        ),
        pd.Series(
            name=f'Ichimoku_ISB_26_{time_tag}',
            data=ichimoku_result[0]['ISB_26']
        ),
        pd.Series(
            name=f'Ichimoku_ITS_9_{time_tag}',
            data=ichimoku_result[0]['ITS_9']
        ),
        pd.Series(
            name=f'Ichimoku_IKS_26_{time_tag}',
            data=ichimoku_result[0]['IKS_26']
        ),
    ]


def parabolic_sar(df, time_tag):
    psar = pta.psar(df['High'], df['Low'], fillna=0)
    return [
        pd.Series(
            name=f'PSAR_PSARl_0.02_0.2_{time_tag}',
            data=psar['PSARl_0.02_0.2']
        ),
        pd.Series(
            name=f'PSARs_0.02_0.2_{time_tag}',
            data=psar['PSARs_0.02_0.2']
        ),
        pd.Series(
            name=f'PSARaf_0.02_0.2_{time_tag}',
            data=psar['PSARaf_0.02_0.2']
        ),
        pd.Series(
            name=f'PSARr_0.02_0.2_{time_tag}',
            data=psar['PSARr_0.02_0.2']
        ),
    ]


def stdev(df, time_tag, length):
    return [pd.Series(
        name=f'Standard_deviation_{length}_{time_tag}',
        data=pta.stdev(df['Close'], length=length)
    )]


def stdev_percentage(df, time_tag, length):
    return [pd.Series(
        name=f'Standard_deviation_Percentage_{length}_{time_tag}',
        data=pta.stdev(df['Close'], length=length) / df['Close']
    )]


def linreg(df, time_tag, length):
    return [pd.Series(
        name=f'Linear_Regression_{length}_{time_tag}',
        data=pta.linreg(df['Close'], length=length)
    )]


def atr(df, time_tag, length):
    return [pd.Series(
        name=f'Average_True_Range_{length}_{time_tag}',
        data=pta.atr(df['High'], df['Low'], df['Close'], length=length)
    )]


def rsi(df, time_tag, length):
    return [pd.Series(
        name=f'rsi_{length}_{time_tag}',
        data=pta.rsi(df['Close'], length=length)
    )]


def cci(df, time_tag, length):
    return [pd.Series(
        name=f'Commodity_Channel_Index_{length}_{time_tag}',
        data=pta.cci(df['High'], df['Low'], df['Close'], length=length)
    )]


def momentum(df, time_tag, length):
    return [pd.Series(
        name=f'Momentum_{length}_{time_tag}',
        data=pta.mom(df['Close'], length=length)
    )]


def macd(df, time_tag):
    macd_result = pta.macd(df['Close'])
    return [
        pd.Series(
            name=f'MACD_12_26_9_{time_tag}',
            data=macd_result['MACD_12_26_9']
        ),
        pd.Series(
            name=f'MACDh_12_26_9_{time_tag}',
            data=macd_result['MACDh_12_26_9']
        ),
        pd.Series(
            name=f'MACDs_12_26_9_{time_tag}',
            data=macd_result['MACDs_12_26_9']
        )
    ]


def stochrsi(df, time_tag, length=14, rsi_length=14):
    stock_rsi = pta.stochrsi(df['Close'], length=length, rsi_length=rsi_length)
    return [
        pd.Series(
            name=f'stoch_rsi_K%_{length}_{time_tag}',
            data=stock_rsi[f'STOCHRSIk_{length}_{rsi_length}_3_3']
        ),
        pd.Series(
            name=f'stoch_rsi_D%_{length}_{time_tag}',
            data=stock_rsi[f'STOCHRSId_{length}_{rsi_length}_3_3']
        )
    ]


def stoch(df, time_tag):
    st = pta.stoch(df['High'], df['Low'], df['Close'])
    return [
        pd.Series(
            name=f'STOCHk_14_3_3_{time_tag}',
            data=st['STOCHk_14_3_3']
        ),
        pd.Series(
            name=f'STOCHd_14_3_3_{time_tag}',
            data=st['STOCHd_14_3_3']
        )
    ]


def rvi(df, time_tag, length):
    return [pd.Series(
        name=f'RVI_{length}_{time_tag}',
        data=pta.rvi(df['Close'], length=length)
    )]


def willr(df, time_tag, length):
    return [pd.Series(
        name=f'William_R_{length}_{time_tag}',
        data=pta.willr(df['High'], df['Low'], df['Close'], length=length)
    )]


def ao(df, time_tag):
    return [pd.Series(
        name=f'Awesome_Oscillator_{time_tag}',
        data=pta.ao(df['High'], df['Low'])
    )]


def ha(df, time_tag):
    heikin_result = pta.ha(df['Open'], df['High'], df['Low'], df['Close'])
    return [
        pd.Series(
            name=f'HA_open_{time_tag}',
            data=heikin_result['HA_open']
        ),
        pd.Series(
            name=f'HA_high_{time_tag}',
            data=heikin_result['HA_high']
        ),
        pd.Series(
            name=f'HA_low_{time_tag}',
            data=heikin_result['HA_low']
        ),
        pd.Series(
            name=f'HA_close_{time_tag}',
            data=heikin_result['HA_close']
        ),
    ]


def donchian(df, time_tag):
    donchian_result = pta.donchian(df['High'], df['Low'])
    return [
        pd.Series(
            name=f'DCL_20_20_{time_tag}',
            data=donchian_result['DCL_20_20']
        ),
        pd.Series(
            name=f'DCM_20_20_{time_tag}',
            data=donchian_result['DCM_20_20']
        ),
        pd.Series(
            name=f'DCU_20_20_{time_tag}',
            data=donchian_result['DCU_20_20']
        ),
    ]


def kelch(df, time_tag, length):
    kelch_m = pd.Series(
        ((df['High'] + df['Low'] + df['Close']) / 3),
        name=f'KelChM_{length}_{time_tag}').rolling(
        window=length).mean()
    kelch_u = pd.Series(
        ((4 * df['High'] - 2 * df['Low'] + df['Close']) / 3),
        name=f'KelChU_{length}_{time_tag}').rolling(
        window=length).mean()
    kelch_d = pd.Series(
        ((-2 * df['High'] + 4 * df['Low'] + df['Close']) / 3),
        name=f'KelChD_{length}_{time_tag}').rolling(
        window=length).mean()
    return [
        pd.Series(
            name=f'KelChM_20_{time_tag}',
            data=kelch_m
        ),
        pd.Series(
            name=f'KelChU_20_{time_tag}',
            data=kelch_u
        ),
        pd.Series(
            name=f'KelChD_20_{time_tag}',
            data=kelch_d
        ),
    ]


def bop(df, time_tag):
    return [pd.Series(
        name=f'Balance_of_power_{time_tag}',
        data=pta.bop(df['Open'], df['High'], df['Low'], df['Close'])
    )]


def uo(df, time_tag):
    return [pd.Series(
        name=f'Ultimate_Oscillator_{time_tag}',
        data=pta.uo(df['High'], df['Low'], df['Close'])
    )]


def accbands(df, time_tag):
    acceleration_bands = pta.accbands(df['High'], df['Low'], df['Close'])
    return [
        pd.Series(
            name=f'ACCBL_20_{time_tag}',
            data=acceleration_bands['ACCBL_20']
        ),
        pd.Series(
            name=f'ACCBM_20_{time_tag}',
            data=acceleration_bands['ACCBM_20']
        ),
        pd.Series(
            name=f'ACCBU_20_{time_tag}',
            data=acceleration_bands['ACCBU_20']
        ),
    ]


def cyclical_datetime(df, time_tag):
    def timefunc(name, sincos, length): return sincos(
        getattr(df.index, name) / length * 2 * np.pi)
    return [
        pd.Series(
            name=f'Day_sin_{time_tag}',
            data=timefunc('day', np.sin, 31),
            index=df.index
        ),
        pd.Series(
            name=f'Day_cos_{time_tag}',
            data=timefunc('day', np.cos, 31),
            index=df.index
        ),
        pd.Series(
            name=f'Month_sin_{time_tag}',
            data=timefunc('month', np.sin, 12),
            index=df.index
        ),
        pd.Series(
            name=f'Month_cos_{time_tag}',
            data=timefunc('month', np.cos, 12),
            index=df.index
        ),
        pd.Series(
            name=f'Hour_sin_{time_tag}',
            data=timefunc('hour', np.sin, 24),
            index=df.index
        ),
        pd.Series(
            name=f'Hour_cos_{time_tag}',
            data=timefunc('hour', np.cos, 24),
            index=df.index
        ),
        pd.Series(
            name=f'Minute_sin_{time_tag}',
            data=timefunc('minute', np.sin, 60),
            index=df.index
        ),
        pd.Series(
            name=f'Minute_cos_{time_tag}',
            data=timefunc('minute', np.cos, 60),
            index=df.index
        ),
        pd.Series(
            name=f'DayOfWeek_sin_{time_tag}',
            data=timefunc('dayofweek', np.sin, 7),
            index=df.index
        ),
        pd.Series(
            name=f'DayOfWeek_cos_{time_tag}',
            data=timefunc('dayofweek', np.cos, 7),
            index=df.index
        ),
    ]


def us_time(df, time_tag):
    return [
        pd.Series(
            name=f'US_time_{time_tag}',
            data=np.logical_or(
                np.logical_and(
                    16 > df.index.hour,
                    df.index.hour >= 10),
                np.logical_and(
                    df.index.hour == 9,
                    df.index.minute >= 30)).astype(int),
            index=df.index)]


def price_log_change(df, time_tag):
    return [
        pd.Series(
            name=f'{col}_log_change_{time_tag}',
            data=log_change(df[col])
        )
        for col in ["Open", "High", "Low", "Close"]
    ]

# Volume indicators
# OBV (on-Balance Volume)


def on_balance_volume(df, time_tag):
    return [pd.Series(
        name=f'Volume_On_Balance_Volume_{time_tag}',
        data=pta.obv(df['Close'], df['Volume'])
    )]

# CMF (Chaikin Money Flow)


def chaikin_money_flow(df, time_tag):
    return [pd.Series(
        name=f'Volume_Chaikin_Money_Flow_{time_tag}',
        data=pta.cmf(df['High'], df['Low'], df['Close'], df['Volume'])
    )]

# Klinger Volume Oscillator


def klinger_oscillator(df, time_tag):
    kvo = pta.kvo(df['High'], df['Low'], df['Close'], df['Volume'])
    return [
        pd.Series(
            name=f'Volume_Chaikin_Money_Flow_{time_tag}',
            data=kvo['KVO_34_55_13']
        ),
        pd.Series(
            name=f'Volume_Chaikin_Money_Flow_s_{time_tag}',
            data=kvo['KVOs_34_55_13']
        )
    ]

# Money Flow index


def money_flow_index(df, time_tag):
    return [pd.Series(
        name=f'Volume_Money_Flow_index_{time_tag}',
        data=pta.mfi(df['High'], df['Low'], df['Close'], df['Volume'])
    )]

# Negative Volume Index


def negative_volume_index(df, time_tag):
    return [pd.Series(
        name=f'Volume_Negative_Volume_index_{time_tag}',
        data=pta.nvi(df['Close'], df['Volume'])
    )]

# Price Volume


def price_volume(df, time_tag):
    return [pd.Series(
        name=f'Volume_Price_Volume_{time_tag}',
        data=pta.pvol(df['Close'], df['Volume'])
    )]

# A/D Oscillator


def ad_oscillator(df, time_tag):
    return [pd.Series(
        name=f'Volume_AD_Oscillator_{time_tag}',
        data=pta.adosc(df['High'], df['Low'], df['Close'], df['Volume'])
    )]

# Ease of movement


def ease_of_movement(df, time_tag):
    return [pd.Series(
        name=f'Volume_Ease_of_movement_{time_tag}',
        data=pta.eom(df['High'], df['Low'], df['Close'], df['Volume'])
    )]

# rsi volume


def rsi_volume(df, time_tag, length):
    return [pd.Series(
        name=f'rsi_volume_{length}_{time_tag}',
        data=pta.rsi(df['Volume'], length=length)
    )]


INDICATORS = dict(
    sma=[10, 20, 50, 100, 200],
    ema=[10, 20, 50, 100, 200],
    dema=[10, 20, 50, 100, 200],
    kama=[10, 20, 50, 100, 200],
    bolinger_bands=None,
    ichimoku=None,
    parabolic_sar=None,
    stdev=[10, 20, 50, 100, 200],
    stdev_percentage=[10, 20, 50, 100, 200],
    linreg=[10, 20, 50, 100, 200],
    atr=[14],
    rsi=[14, 26],
    cci=[20, 50],
    momentum=[10, 14, 21],
    macd=None,
    stochrsi=[14, [46, 46]],
    stoch=None,
    rvi=[14],
    willr=[14],
    ao=None,
    ha=None,
    donchian=None,
    kelch=[20],
    bop=None,
    uo=None,
    accbands=None,
    cyclical_datetime=None,
    us_time=None,
    price_log_change=None,
    on_balance_volume=None,
    chaikin_money_flow=None,
    klinger_oscillator=None,
    money_flow_index=None,
    negative_volume_index=None,
    price_volume=None,
    ad_oscillator=None,
    ease_of_movement=None,
    rsi_volume=[5, 14, 26]
)


def add_technical_indicators(dataset, time_tag, show_progress=True):
    df = dataset.df if isinstance(dataset, Dataset) else dataset
    collected_indicators = [df]
    if show_progress:
        pbar = tqdm(total=len(INDICATORS.items()))
    for indicator, params in INDICATORS.items():
        if show_progress:
            pbar.set_description(f'Adding {indicator}')
        indicator_func = getattr(sys.modules[__name__], indicator)
        if params is None:
            collected_indicators.extend(indicator_func(df, time_tag))
        else:
            for param in params:
                if isinstance(param, list):
                    collected_indicators.extend(
                        indicator_func(df, time_tag, *param))
                elif isinstance(param, dict):
                    collected_indicators.extend(
                        indicator_func(df, time_tag, **param))
                else:
                    collected_indicators.extend(
                        indicator_func(df, time_tag, param))
        if show_progress:
            pbar.update()
    if show_progress:
        pbar.close()
    return pd.concat(collected_indicators, axis=1)
