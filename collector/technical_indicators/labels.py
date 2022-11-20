import sys

import numpy as np
import pandas as pd
import bisect
from commons.data.dataset import Dataset
import logging
from tqdm import tqdm

LOGGER = logging.getLogger(__name__)


def add_best_decision(dataset: Dataset, pct_change):
    next_long = find_indexes_with_price_percentage_change(
        dataset.df, pct_change, direction=1)
    next_short = find_indexes_with_price_percentage_change(
        dataset.df, pct_change, direction=-1)
    next_long = next_long.apply(lambda x: x.value if x is not None else np.inf)
    next_short = next_short.apply(
        lambda x: x.value if x is not None else np.inf)
    dataset.add_label(f'Best_decision_{pct_change}', np.argmin(np.concatenate(
        [np.expand_dims(next_short, 1), np.expand_dims(next_long, 1)], axis=1), axis=1))


def find_indexes_with_price_percentage_change(
        df: pd.DataFrame, pct_change, direction):
    result = {}
    hanging = []
    furthest_col = 'High' if direction == 1 else 'Low'
    LOGGER.info(
        f"Finding indexes with price percentage change for pct_change={pct_change} and direction={direction}")
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        while hanging and direction * \
                row[furthest_col] >= direction * hanging[0]['price'] * (1 + direction * pct_change):
            top = hanging.pop(0)
            result[top['index']] = index
        insert(hanging, {'index': index, 'price': row['Close']}, direction)
    result_df = pd.DataFrame(index=df.index.copy())
    result_df['result'] = None
    for k, v in result.items():
        result_df['result'][k] = v
    return result_df['result']


def insert(s, element, direction):
    prices = [direction * entry['price'] for entry in s]
    idx = bisect.bisect(prices, direction * element['price'])
    s.insert(idx, element)


LABELS = dict(
    add_best_decision=[0.01],
)


def add_labels(dataset: Dataset):
    for label, params in LABELS.items():
        label_func = getattr(sys.modules[__name__], label)
        if params is None:
            label_func(dataset)
        else:
            for param in params:
                if isinstance(param, list):
                    label_func(dataset, *param)
                elif isinstance(param, dict):
                    label_func(dataset, **param)
                else:
                    label_func(dataset, param)
