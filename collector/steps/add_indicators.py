import logging
import yaml
from tqdm import tqdm
import pandas as pd
import core.data.indicators as inds


LOGGER = logging.getLogger(__name__)
DEFAULT_INDICATOR_CONFIG = dict(
    sma=[10, 20],
    stdev=[10, 20],
    atr=[14],
    rsi=[14, 26],
    momentum=[10, 14, 21],
    stoch=None,
    rvi=[14],
    willr=[14],
    ha=None,
    donchian=None,
    kelch=[20],
    bop=None,
    cyclical_datetime=None,
    us_time=None,
    on_balance_volume=None,
    chaikin_money_flow=None,
    money_flow_index=None,
    negative_volume_index=None,
    price_volume=None,
    ad_oscillator=None,
    ease_of_movement=None,
    rsi_volume=[5, 14, 26],
    vwap=None
)


def add_indicators(dataset, indicators=None, indicator_config=None, show_progress=True, **kwargs):
    dataset.df = dataset.df.asfreq("1min")
    if indicators is not None:
        with open(indicators, 'r') as f:
            indicator_config = yaml.load(f, yaml.CLoader)
    if indicator_config is None:
        indicator_config = DEFAULT_INDICATOR_CONFIG
    time_tag = f"{dataset.interval.total_seconds():.0f}s"
    df = dataset.df
    collected_indicators = [df]
    if show_progress:
        pbar = tqdm(total=len(indicator_config.items()))
    for indicator, params in indicator_config.items():
        if show_progress:
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
        if show_progress:
            pbar.update()
    if show_progress:
        pbar.close()
    dataset.df = pd.concat(collected_indicators, axis=1)
