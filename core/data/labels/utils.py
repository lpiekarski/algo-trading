import bisect
import pandas as pd
import logging
from tqdm import tqdm


LOGGER = logging.getLogger(__name__)


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
