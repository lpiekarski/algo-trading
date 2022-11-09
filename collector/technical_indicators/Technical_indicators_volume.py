import sys

import pandas as pd
import pandas_ta as pta
import numpy as np

from commons.data.dataset import Dataset


# OBV (on-Balance Volume)
def add_On_Balance_Volume(df, time_tag):
    df[f'Volume_On_Balance_Volume_{time_tag}'] = pta.obv(df['Close'], df['Volume'])

# CMF (Chaikin Money Flow)
def add_Chaikin_Money_Flow(df, time_tag):
    df[f'Volume_Chaikin_Money_Flow_{time_tag}'] = pta.cmf(df['High'], df['Low'], df['Close'], df['Volume'])

# Klinger Volume Oscillator
def add_Klinger_Oscillator(df, time_tag):
    kvo = pta.kvo(df['High'], df['Low'], df['Close'], df['Volume'])
    df[f'Volume_Chaikin_Money_Flow_{time_tag}'] = kvo['KVO_34_55_13']
    df[f'Volume_Chaikin_Money_Flow_s_{time_tag}'] = kvo['KVOs_34_55_13']

# Money Flow index
def add_Money_Flow_index(df, time_tag):
    df[f'Volume_Money_Flow_index_{time_tag}'] = pta.mfi(df['High'], df['Low'], df['Close'], df['Volume'])

# Negative Volume Index
def add_Negative_Volume_index(df, time_tag):
    df[f'Volume_Negative_Volume_index_{time_tag}'] = pta.nvi(df['Close'], df['Volume'])

# Price Volume
def add_Price_Volume(df, time_tag):
    df[f'Volume_Price_Volume_{time_tag}'] = pta.pvol(df['Close'], df['Volume'])

# A/D Oscillator
def add_AD_Oscillator(df, time_tag):
    df[f'Volume_AD_Oscillator_{time_tag}'] = pta.adosc(df['High'], df['Low'], df['Close'], df['Volume'])

# Ease of movement
def add_Ease_of_movement(df, time_tag):
    df[f'Volume_Ease_of_movement_{time_tag}'] = pta.eom(df['High'], df['Low'], df['Close'], df['Volume'])


VOLUME_INDICATORS = dict(
    add_On_Balance_Volume=None,
    add_Chaikin_Money_Flow=None,
    add_Klinger_Oscillator=None,
    add_Money_Flow_index=None,
    add_Negative_Volume_index=None,
    add_Price_Volume=None,
    add_AD_Oscillator=None,
    add_Ease_of_movement=None
)


def add_technical_indicators(dataset, time_tag):
    df = dataset.df if isinstance(dataset, Dataset) else dataset
    for indicator, params in VOLUME_INDICATORS.items():
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
