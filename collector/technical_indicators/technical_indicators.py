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

# add technical indicators for all
def ADD_technical_indicators(df, time_tag):
    ### Trend indicators:
    # Moving average
    df[f'SMA_10_{time_tag}'] = pta.sma(df["Close"], length=10)
    df[f'SMA_20_{time_tag}'] = pta.sma(df["Close"], length=20)
    df[f'SMA_50_{time_tag}'] = pta.sma(df["Close"], length=50)
    df[f'SMA_100_{time_tag}'] = pta.sma(df["Close"], length=100)
    df[f'SMA_200_{time_tag}'] = pta.sma(df["Close"], length=200)

    # Exponential moving average
    df[f'EMA_10_{time_tag}'] = pta.ema(df["Close"], length=10)
    df[f'EMA_20_{time_tag}'] = pta.ema(df["Close"], length=20)
    df[f'EMA_50_{time_tag}'] = pta.ema(df["Close"], length=50)
    df[f'EMA_100_{time_tag}'] = pta.ema(df["Close"], length=100)
    df[f'EMA_200_{time_tag}'] = pta.ema(df["Close"], length=200)

    # Double Exponential moving average
    df[f'DEMA_10_{time_tag}'] = pta.dema(df["Close"], length=10)
    df[f'DEMA_20_{time_tag}'] = pta.dema(df["Close"], length=20)
    df[f'DEMA_50_{time_tag}'] = pta.dema(df["Close"], length=50)
    df[f'DEMA_100_{time_tag}'] = pta.dema(df["Close"], length=100)
    df[f'DEMA_200_{time_tag}'] = pta.dema(df["Close"], length=200)

    # Kaufman's Adaptive Moving Average
    df[f'kama_10_{time_tag}'] = pta.kama(df["Close"], length=10)
    df[f'kama_20_{time_tag}'] = pta.kama(df["Close"], length=20)
    df[f'kama_50_{time_tag}'] = pta.kama(df["Close"], length=50)
    df[f'kama_100_{time_tag}'] = pta.kama(df["Close"], length=100)
    df[f'kama_200_{time_tag}'] = pta.kama(df["Close"], length=200)

    # Bolinger Bands
    bbands_result = pta.bbands(df["Close"], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    df[f'Upperband_{time_tag}'] = bbands_result['BBL_5_2.0']
    df[f'Middleband_{time_tag}'] = bbands_result['BBM_5_2.0']
    df[f'Lowerband_{time_tag}'] = bbands_result['BBU_5_2.0']
    df[f'Bandwidth_{time_tag}'] = bbands_result['BBB_5_2.0']
    df[f'Percent_Column_BBands_{time_tag}'] = bbands_result['BBP_5_2.0']

    # Ichimoku
    ichimoku_result = pta.ichimoku(df['High'], df['Low'], df['Close'])
    df[f'Ichimoku_ISA_9_{time_tag}'] = ichimoku_result[0]['ISA_9']
    df[f'Ichimoku_ISB_26_{time_tag}'] = ichimoku_result[0]['ISB_26']
    df[f'Ichimoku_ITS_9_{time_tag}'] = ichimoku_result[0]['ITS_9']
    df[f'Ichimoku_IKS_26_{time_tag}'] = ichimoku_result[0]['IKS_26']

    # Parabolic SAR
    PSAR = pta.psar(df['High'], df['Low'])
    df[f'PSAR_PSARl_0.02_0.2_{time_tag}'] = PSAR['PSARl_0.02_0.2']
    df[f'PSARs_0.02_0.2_{time_tag}'] = PSAR['PSARs_0.02_0.2']
    df[f'PSARaf_0.02_0.2_{time_tag}'] = PSAR['PSARaf_0.02_0.2']
    df[f'PSARr_0.02_0.2_{time_tag}'] = PSAR['PSARr_0.02_0.2']

    # Standard deviation
    df[f'Standard_deviation_10_{time_tag}'] = pta.stdev(df['Close'], length=10)
    df[f'Standard_deviation_20_{time_tag}'] = pta.stdev(df['Close'], length=20)
    df[f'Standard_deviation_50_{time_tag}'] = pta.stdev(df['Close'], length=50)
    df[f'Standard_deviation_100_{time_tag}'] = pta.stdev(df['Close'], length=100)
    df[f'Standard_deviation_200_{time_tag}'] = pta.stdev(df['Close'], length=200)

    # Regression
    df[f'Linear_Regression_10_{time_tag}'] = pta.linreg(df['Close'], length=10)
    df[f'Linear_Regression_20_{time_tag}'] = pta.linreg(df['Close'], length=20)
    df[f'Linear_Regression_50_{time_tag}'] = pta.linreg(df['Close'], length=50)
    df[f'Linear_Regression_100_{time_tag}'] = pta.linreg(df['Close'], length=100)
    df[f'Linear_Regression_200_{time_tag}'] = pta.linreg(df['Close'], length=200)

    # more?
    ###Oscillators:
    # Average True Range
    df[f'Average_True_Range_14_{time_tag}'] = pta.atr(df['High'], df['Low'], df['Close'], length=14)

    # RSI 14
    df[f'rsi_14_{time_tag}'] = pta.rsi(df['Close'], length=14)
    df[f'rsi_26_{time_tag}'] = pta.rsi(df['Close'], length=26)

    # Commodity Channel Index
    df[f'Commodity_Channel_Index_20_{time_tag}'] = pta.cci(df['High'], df['Low'], df['Close'], length=20)
    df[f'Commodity_Channel_Index_50_{time_tag}'] = pta.cci(df['High'], df['Low'], df['Close'], length=50)

    # Momentum
    df[f'Momentum_10_{time_tag}'] = pta.mom(df['Close'], length=10)
    df[f'Momentum_14_{time_tag}'] = pta.mom(df['Close'], length=14)
    df[f'Momentum_21_{time_tag}'] = pta.mom(df['Close'], length=21)

    # MACD
    macd_result = pta.macd(df['Close'])
    df[f'MACD_12_26_9_{time_tag}'] = macd_result['MACD_12_26_9']
    df[f'MACDh_12_26_9_{time_tag}'] = macd_result['MACDh_12_26_9']
    df[f'MACDs_12_26_9_{time_tag}'] = macd_result['MACDs_12_26_9']

    # Stochastic RSI
    Stoch_RSI = pta.stochrsi(df['Close'], length=14)
    df[f'stoch_rsi_K%_14_{time_tag}'] = Stoch_RSI['STOCHRSIk_14_14_3_3']
    df[f'stoch_rsi_D%_14_{time_tag}'] = Stoch_RSI['STOCHRSId_14_14_3_3']
    Stoch_RSI = pta.stochrsi(df['Close'], length=46, rsi_length=46)
    df[f'stoch_rsi_K%_46_{time_tag}'] = Stoch_RSI['STOCHRSIk_46_46_3_3']
    df[f'stoch_rsi_D%_46_{time_tag}'] = Stoch_RSI['STOCHRSId_46_46_3_3']

    # Stochastic
    Stoch = pta.stoch(df['High'], df['Low'], df['Close'])
    df[f'STOCHk_14_3_3_{time_tag}'] = Stoch['STOCHk_14_3_3']
    df[f'STOCHd_14_3_3_{time_tag}'] = Stoch['STOCHd_14_3_3']

    # Relative Vigor Index
    df[f'RVI_14_{time_tag}'] = pta.rvi(df['Close'], length=14)

    # R Williams
    df[f'William_R_14_{time_tag}'] = pta.willr(df['High'], df['Low'], df['Close'], length=14)

    ###Volumes ?
    ### others: (mainly mixes of both)
    # Awesome Oscillator
    df[f'Awesome_Oscillator_{time_tag}'] = pta.ao(df['High'], df['Low'], )

    # Heikin Ashi
    heikin_result = pta.ha(df['Open'], df['High'], df['Low'], df['Close'])
    df[f'HA_open_{time_tag}'] = heikin_result['HA_open']
    df[f'HA_high_{time_tag}'] = heikin_result['HA_high']
    df[f'HA_low_{time_tag}'] = heikin_result['HA_low']
    df[f'HA_close_{time_tag}'] = heikin_result['HA_close']

    # Donchian Channel
    donchian_result = pta.donchian(df['High'], df['Low'])
    df[f'DCL_20_20_{time_tag}'] = donchian_result['DCL_20_20']
    df[f'DCM_20_20_{time_tag}'] = donchian_result['DCM_20_20']
    df[f'DCU_20_20_{time_tag}'] = donchian_result['DCU_20_20']

    # Keltner Channel
    kelch = KELCH(df, 20)
    df[f'KelChM_20_{time_tag}'] = kelch['KelChM_20']
    df[f'KelChU_20_{time_tag}'] = kelch['KelChU_20']
    df[f'KelChD_20_{time_tag}'] = kelch['KelChD_20']

    # Balance of power
    df[f'Balance_of_power_{time_tag}'] = pta.bop(df['Open'], df['High'], df['Low'], df['Close'])

    # Ultimate oscillator
    df[f'Ultimate_Oscillator_{time_tag}'] = pta.uo(df['High'], df['Low'], df['Close'])

    # Acceleration Bands
    acceleration_bands = pta.accbands(df['High'], df['Low'], df['Close'])
    df[f'ACCBL_20_{time_tag}'] = acceleration_bands['ACCBL_20']
    df[f'ACCBM_20_{time_tag}'] = acceleration_bands['ACCBM_20']
    df[f'ACCBU_20_{time_tag}'] = acceleration_bands['ACCBU_20']

    return df
