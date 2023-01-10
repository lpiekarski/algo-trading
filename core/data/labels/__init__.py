from core.data.dataset import Dataset
from core.data.labels.utils import find_indexes_with_price_percentage_change
import numpy as np


def best_decision(dataset: Dataset, pct_change):
    next_long = find_indexes_with_price_percentage_change(
        dataset.df, pct_change, direction=1)
    next_short = find_indexes_with_price_percentage_change(
        dataset.df, pct_change, direction=-1)
    next_long = next_long.apply(lambda x: x.value if x is not None else np.inf)
    next_short = next_short.apply(
        lambda x: x.value if x is not None else np.inf)
    dataset.add_label(f'Best_decision_{pct_change}', np.argmin(np.concatenate(
        [np.expand_dims(next_short, 1), np.expand_dims(next_long, 1)], axis=1), axis=1))
