import logging
import yaml
from tqdm import tqdm
from commons.timing import step
import sys
import pandas as pd
import commons.data.indicators as inds


LOGGER = logging.getLogger(__name__)
DEFAULT_INDICATOR_CONFIG = dict(
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


@step
def add_indicators(dataset, indicators=None, **kwargs):
    indicator_config = None
    if indicators is not None:
        with open(indicators, 'r') as f:
            indicator_config = yaml.load(f, yaml.CLoader)
    if indicator_config is None:
        indicator_config = DEFAULT_INDICATOR_CONFIG
    time_tag = f"{dataset.interval.total_seconds():.0f}s"
    df = dataset.df
    collected_indicators = [df]
    pbar = tqdm(total=len(indicator_config.items()))
    for indicator, params in indicator_config.items():
        pbar.set_description(f'Adding {indicator}')
        indicator_func = getattr(inds, indicator)
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
        pbar.update()
    pbar.close()
    dataset.df = pd.concat(collected_indicators, axis=1)
