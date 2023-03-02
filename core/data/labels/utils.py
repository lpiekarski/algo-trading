import bisect
from sortedcontainers import SortedDict

import pandas as pd
import logging
from tqdm import tqdm
import numpy as np

from core.data.dataset import Dataset

LOGGER = logging.getLogger(__name__)


def get_weighted_best_decision(dataset: Dataset, pct_change: float, smoothing_number: int = 60):
    next_long = find_indexes_with_price_percentage_change(
        dataset.df, pct_change, direction=1)
    next_short = find_indexes_with_price_percentage_change(
        dataset.df, pct_change, direction=-1)

    next_long = next_long.apply(lambda x: x.value if x is not None else np.inf)
    next_short = next_short.apply(
        lambda x: x.value if x is not None else np.inf)

    seconds_to_next_long = (next_long - next_long.index.values.astype("float64")) / (10**9 * 60)
    seconds_to_next_short = (next_short - next_short.index.values.astype("float64")) / (10**9 * 60)

    decision = np.array(seconds_to_next_long)
    mask = seconds_to_next_long > seconds_to_next_short
    decision[mask] = -seconds_to_next_short[mask]
    decision = smoothing_number / decision
    decision = 1 / (1 + np.exp(-decision))
    return decision


def find_indexes_with_price_percentage_change(
        df: pd.DataFrame, pct_change: float, direction: int):
    result = {}
    hanging = SortedDict()
    furthest_col = 'High' if direction == 1 else 'Low'
    LOGGER.info(
        f"Finding indexes with price percentage change for pct_change={pct_change} and direction={direction}")
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        if np.isnan(row["Close"]):
            continue
        while True:
            if not hanging:
                break
            top_price, top_idx = next(iter(hanging.items()))
            if direction * row[furthest_col] >= top_price * (1 + direction * pct_change):
                hanging.pop(top_price)
                result[top_idx] = index
            else:
                break
        hanging[row['Close'] * direction] = index
    result_df = pd.DataFrame(index=df.index.copy())
    result_df['result'] = None
    for k, v in result.items():
        result_df['result'][k] = v
    return result_df['result']
