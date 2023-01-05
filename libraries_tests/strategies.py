import pandas_ta as ta

MyStrategy = ta.Strategy(
    name="strategy",
    description="i don't fucking care",
    ta=[
        {"kind": "sma", "length": 10},
        # {"kind": "sma", "length": 20},
        {"kind": "sma", "length": 50},
        {"kind": "sma", "length": 100},
        {"kind": "sma", "length": 200},

        {"kind": "ema", "length": 10},
        {"kind": "ema", "length": 20},# df = df[['Close','Open','High']]
# df.ta.sma('Close',length=10)
# print(df.tail(10))
# x = ta.sma(df["Close"], length=40)

        {"kind": "ema", "length": 50},
        {"kind": "ema", "length": 100},
        {"kind": "ema", "length": 200},

        {"kind": "dema", "length": 10},
        {"kind": "dema", "length": 20},
        {"kind": "dema", "length": 50},
        {"kind": "dema", "length": 100},
        {"kind": "dema", "length": 200},

        {"kind": "kama", "length": 10},
        {"kind": "kama", "length": 20},
        {"kind": "kama", "length": 50},
        {"kind": "kama", "length": 100},
        {"kind": "kama", "length": 200},

        # {"kind": "bbands",  "timeperiod": 20, "nbdevup": 2, "nbdevdn": 2, "matype": 0},

        {"kind": "ichimoku"},

        {"kind": "psar", "fillna": 0},

        {"kind": "stdev", "length": 10},
        {"kind": "stdev", "length": 20},
        {"kind": "stdev", "length": 50},
        {"kind": "stdev", "length": 100},
        {"kind": "stdev", "length": 200},

        {"kind": "linreg", "length": 10},
        {"kind": "linreg", "length": 20},
        {"kind": "linreg", "length": 50},
        {"kind": "linreg", "length": 100},
        {"kind": "linreg", "length": 200},

        {"kind": "atr", "length": 14},
        {"kind": "rsi", "length": 26},
        {"kind": "cci", "length": 20},
        {"kind": "cci", "length": 50},

        {"kind": "mom", "length": 10},
        {"kind": "mom", "length": 14},
        {"kind": "mom", "length": 21},
        {"kind": "macd"},
        {"kind": "stoch"},
        {"kind": "rvi", "length": 16},
        {"kind": "willr", "length": 14},
        {"kind": "ao"},
        {"kind": "ha"},
        {"kind": "donchian"},
        {"kind": "bop"},
        {"kind": "uo"},
        {"kind": "accbands"},
        {"kind": "obv"},
        {"kind": "cmf"},
        {"kind": "kvo"},
        {"kind": "mfi"},
        {"kind": "nvi"},
        {"kind": "pvol"},
        {"kind": "adosc"},
        {"kind": "eom"},
        {"kind": "rsi", "close": "volume", "length": 5, "prefix": "VOLUME"},
        {"kind": "rsi", "close": "volume", "length": 14, "prefix": "VOLUME"},
        {"kind": "rsi", "close": "volume", "length": 26, "prefix": "VOLUME"},
        {"kind": "vwap"}
    ]
)

INDICATORS2 = dict(
    sma=[10, 20, 50, 100, 200],
    ema=[10, 20, 50, 100, 200],
    dema=[10, 20, 50, 100, 200],
    kama=[10, 20, 50, 100, 200],
    bolinger_bands=None,
    ichimoku=None,
    parabolic_sar=None,
    stdev=[10, 20, 50, 100, 200],
    # stdev_percentage=[10, 20, 50, 100, 200], our variation
    linreg=[10, 20, 50, 100, 200],
    atr=[14],
    rsi=[14, 26],
    cci=[20, 50],
    momentum=[10, 14, 21],
    macd=None,
    # stochrsi=[14, [46, 46]], ??
    stoch=None,
    rvi=[14],
    willr=[14],
    ao=None,
    ha=None,
    donchian=None,
    # kelch=[20], our variation
    bop=None,
    uo=None,
    accbands=None,
    # cyclical_datetime=None, our variation
    # us_time=None, our variation
    on_balance_volume=None,
    chaikin_money_flow=None,
    klinger_oscillator=None,
    money_flow_index=None,
    negative_volume_index=None,
    price_volume=None,
    ad_oscillator=None,
    ease_of_movement=None,
    rsi_volume=[5, 14, 26],
    vwap=None
)