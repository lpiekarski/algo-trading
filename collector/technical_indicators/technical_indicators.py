# libraries
import pandas as pd
import pandas_ta as pta

# Keltner Channel
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
    return df

def add_ema(df, time_tag, length):
    df[f'EMA_{length}_{time_tag}'] = pta.ema(df["Close"], length=length)
    return df

def add_dema(df, time_tag, length):
    df[f'DEMA_{length}_{time_tag}'] = pta.dema(df["Close"], length=length)
    return df

def add_kama(df, time_tag, length):
    df[f'kama_{length}_{time_tag}'] = pta.kama(df["Close"], length=length)
    return df

def add_bolinger_bands(df, time_tag):
    bbands_result = pta.bbands(df["Close"], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    df[f'Upperband_{time_tag}'] = bbands_result['BBL_5_2.0']
    df[f'Middleband_{time_tag}'] = bbands_result['BBM_5_2.0']
    df[f'Lowerband_{time_tag}'] = bbands_result['BBU_5_2.0']
    df[f'Bandwidth_{time_tag}'] = bbands_result['BBB_5_2.0']
    df[f'Percent_Column_BBands_{time_tag}'] = bbands_result['BBP_5_2.0']
    return df

def add_ichimoku(df, time_tag):
    ichimoku_result = pta.ichimoku(df['High'], df['Low'], df['Close'])
    df[f'Ichimoku_ISA_9_{time_tag}'] = ichimoku_result[0]['ISA_9']
    df[f'Ichimoku_ISB_26_{time_tag}'] = ichimoku_result[0]['ISB_26']
    df[f'Ichimoku_ITS_9_{time_tag}'] = ichimoku_result[0]['ITS_9']
    df[f'Ichimoku_IKS_26_{time_tag}'] = ichimoku_result[0]['IKS_26']
    return df

def add_parabolic_sar(df, time_tag):
    PSAR = pta.psar(df['High'], df['Low'])
    df[f'PSAR_PSARl_0.02_0.2_{time_tag}'] = PSAR['PSARl_0.02_0.2']
    df[f'PSARs_0.02_0.2_{time_tag}'] = PSAR['PSARs_0.02_0.2']
    df[f'PSARaf_0.02_0.2_{time_tag}'] = PSAR['PSARaf_0.02_0.2']
    df[f'PSARr_0.02_0.2_{time_tag}'] = PSAR['PSARr_0.02_0.2']
    return df

def add_stdev(df, time_tag, length):
    df[f'Standard_deviation_{length}_{time_tag}'] = pta.stdev(df['Close'], length=length)
    return df

def add_linreg(df, time_tag, length):
    df[f'Linear_Regression_{length}_{time_tag}'] = pta.linreg(df['Close'], length=length)
    return df

def add_atr(df, time_tag, length):
    df[f'Average_True_Range_{length}_{time_tag}'] = pta.atr(df['High'], df['Low'], df['Close'], length=length)
    return df

def add_rsi(df, time_tag, length):
    df[f'rsi_{length}_{time_tag}'] = pta.rsi(df['Close'], length=length)
    return df

def add_cci(df, time_tag, length):
    df[f'Commodity_Channel_Index_{length}_{time_tag}'] = pta.cci(df['High'], df['Low'], df['Close'], length=length)
    return df


def add_momentum(df, time_tag, length):
    df[f'Momentum_{length}_{time_tag}'] = pta.mom(df['Close'], length=length)
    return df

def add_macd(df, time_tag):
    macd_result = pta.macd(df['Close'])
    df[f'MACD_12_26_9_{time_tag}'] = macd_result['MACD_12_26_9']
    df[f'MACDh_12_26_9_{time_tag}'] = macd_result['MACDh_12_26_9']
    df[f'MACDs_12_26_9_{time_tag}'] = macd_result['MACDs_12_26_9']
    return df

def add_stochrsi(df, time_tag, length=14, rsi_length=14):
    Stoch_RSI = pta.stochrsi(df['Close'], length=length, rsi_length=rsi_length)
    df[f'stoch_rsi_K%_{length}_{time_tag}'] = Stoch_RSI[f'STOCHRSIk_{length}_{rsi_length}_3_3']
    df[f'stoch_rsi_D%_{length}_{time_tag}'] = Stoch_RSI[f'STOCHRSId_{length}_{rsi_length}_3_3']
    return df

def add_stoch(df, time_tag):
    Stoch = pta.stoch(df['High'], df['Low'], df['Close'])
    df[f'STOCHk_14_3_3_{time_tag}'] = Stoch['STOCHk_14_3_3']
    df[f'STOCHd_14_3_3_{time_tag}'] = Stoch['STOCHd_14_3_3']
    return df

def add_rvi(df, time_tag, length):
    df[f'RVI_{length}_{time_tag}'] = pta.rvi(df['Close'], length=length)
    return df

def add_willr(df, time_tag, length):
    df[f'William_R_{length}_{time_tag}'] = pta.willr(df['High'], df['Low'], df['Close'], length=length)
    return df

def add_ao(df, time_tag):
    df[f'Awesome_Oscillator_{time_tag}'] = pta.ao(df['High'], df['Low'], )
    return df

def add_ha(df, time_tag):
    heikin_result = pta.ha(df['Open'], df['High'], df['Low'], df['Close'])
    df[f'HA_open_{time_tag}'] = heikin_result['HA_open']
    df[f'HA_high_{time_tag}'] = heikin_result['HA_high']
    df[f'HA_low_{time_tag}'] = heikin_result['HA_low']
    df[f'HA_close_{time_tag}'] = heikin_result['HA_close']
    return df

def add_donchian(df, time_tag):
    donchian_result = pta.donchian(df['High'], df['Low'])
    df[f'DCL_20_20_{time_tag}'] = donchian_result['DCL_20_20']
    df[f'DCM_20_20_{time_tag}'] = donchian_result['DCM_20_20']
    df[f'DCU_20_20_{time_tag}'] = donchian_result['DCU_20_20']
    return df

def add_KELCH(df, time_tag):
    kelch = KELCH(df, 20)
    df[f'KelChM_20_{time_tag}'] = kelch['KelChM_20']
    df[f'KelChU_20_{time_tag}'] = kelch['KelChU_20']
    df[f'KelChD_20_{time_tag}'] = kelch['KelChD_20']
    return df

def add_bop(df, time_tag):
    df[f'Balance_of_power_{time_tag}'] = pta.bop(df['Open'], df['High'], df['Low'], df['Close'])
    return df

def add_uo(df, time_tag):
    df[f'Ultimate_Oscillator_{time_tag}'] = pta.uo(df['High'], df['Low'], df['Close'])
    return df

def add_accbands(df, time_tag):
    acceleration_bands = pta.accbands(df['High'], df['Low'], df['Close'])
    df[f'ACCBL_20_{time_tag}'] = acceleration_bands['ACCBL_20']
    df[f'ACCBM_20_{time_tag}'] = acceleration_bands['ACCBM_20']
    df[f'ACCBU_20_{time_tag}'] = acceleration_bands['ACCBU_20']
    return df

# add technical indicators for all
def add_technical_indicators(df, time_tag):
    ### Trend indicators:
    # Moving average
    df = add_sma(df, time_tag, 10)
    df = add_sma(df, time_tag, 20)
    df = add_sma(df, time_tag, 50)
    df = add_sma(df, time_tag, 100)
    df = add_sma(df, time_tag, 200)

    # Exponential moving average
    df = add_ema(df, time_tag, 10)
    df = add_ema(df, time_tag, 20)
    df = add_ema(df, time_tag, 50)
    df = add_ema(df, time_tag, 100)
    df = add_ema(df, time_tag, 200)

    # Double Exponential moving average
    df = add_dema(df, time_tag, 10)
    df = add_dema(df, time_tag, 20)
    df = add_dema(df, time_tag, 50)
    df = add_dema(df, time_tag, 100)
    df = add_dema(df, time_tag, 200)

    # Kaufman's Adaptive Moving Average
    df = add_kama(df, time_tag, 10)
    df = add_kama(df, time_tag, 20)
    df = add_kama(df, time_tag, 50)
    df = add_kama(df, time_tag, 100)
    df = add_kama(df, time_tag, 200)

    # Bolinger Bands
    df = add_bolinger_bands(df, time_tag)

    # Ichimoku
    df = add_ichimoku(df, time_tag)

    # Parabolic SAR
    df = add_parabolic_sar(df, time_tag)

    # Standard deviation
    df = add_stdev(df, time_tag, 10)
    df = add_stdev(df, time_tag, 20)
    df = add_stdev(df, time_tag, 50)
    df = add_stdev(df, time_tag, 100)
    df = add_stdev(df, time_tag, 200)

    # Regression
    df = add_linreg(df, time_tag, 10)
    df = add_linreg(df, time_tag, 20)
    df = add_linreg(df, time_tag, 50)
    df = add_linreg(df, time_tag, 100)
    df = add_linreg(df, time_tag, 200)

    # more?
    ###Oscillators:
    # Average True Range
    df = add_atr(df, time_tag, 14)

    # RSI 14
    df = add_rsi(df, time_tag, 14)
    df = add_rsi(df, time_tag, 26)

    # Commodity Channel Index
    df = add_cci(df, time_tag, 20)
    df = add_cci(df, time_tag, 50)

    # Momentum
    df = add_momentum(df, time_tag, 10)
    df = add_momentum(df, time_tag, 14)
    df = add_momentum(df, time_tag, 21)

    # MACD
    df = add_macd(df, time_tag)

    # Stochastic RSI
    df = add_stochrsi(df, time_tag, 14)
    df = add_stochrsi(df, time_tag, length=46, rsi_length=46)

    # Stochastic
    df = add_stoch(df, time_tag)

    # Relative Vigor Index
    df = add_rvi(df, time_tag, 14)

    # R Williams
    df = add_willr(df, time_tag, 14)

    ###Volumes ?
    ### others: (mainly mixes of both)
    # Awesome Oscillator
    df = add_ao(df, time_tag)

    # Heikin Ashi
    df = add_ha(df, time_tag)

    # Donchian Channel
    df = add_donchian(df, time_tag)

    # Keltner Channel
    df = add_KELCH(df, time_tag)

    # Balance of power
    df = add_bop(df, time_tag)

    # Ultimate oscillator
    df = add_uo(df, time_tag)

    # Acceleration Bands
    df = add_accbands(df, time_tag)

    return df

def actual_technical_indicators(df_h, df_actual, time_tag="hoour", high=0, low=0):
    df_supp = df_h.append(df_actual.iloc[-1])
    return add_technical_indicators(df_supp, "actual")