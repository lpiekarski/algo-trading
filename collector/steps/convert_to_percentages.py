from tqdm import tqdm

from core.data.dataset import Dataset
import pandas as pd


def convert_to_percentages(percentage: str, dataset_name: str, dataset: Dataset, **kwargs):
    percentage = float(percentage)
    result = dict(Open=[], High=[], Low=[], Close=[], std=[], Volume=[], duration=[])
    result_dates = []
    reversed_df = dataset.df[::-1]
    start_idx = 0
    start_close = reversed_df.iloc[start_idx]["Close"]
    for idx in tqdm(range(reversed_df.shape[0])):
        row = reversed_df.iloc[idx]
        current_high = row["High"]
        current_low = row["Low"]
        if current_high / start_close - 1 >= percentage or 1 - current_low / start_close >= percentage:
            result["Open"].append(reversed_df.iloc[idx - 1]["Open"])
            result["Close"].append(reversed_df.iloc[start_idx]["Close"])
            result["Low"].append(reversed_df.iloc[start_idx:idx]["Low"].min())
            result["High"].append(reversed_df.iloc[start_idx:idx]["High"].max())
            result["Volume"].append(reversed_df.iloc[start_idx:idx]["Volume"].sum())
            result["std"].append(reversed_df.iloc[start_idx:idx]["Close"].std())
            result["duration"].append((reversed_df.index[start_idx] - reversed_df.index[idx - 1]).total_seconds())
            result_dates.append(reversed_df.index[idx - 1])
            start_idx = idx
            start_close = reversed_df.iloc[start_idx]["Close"]
    return dict(
        dataset=Dataset(pd.DataFrame(data=result, index=result_dates)[::-1])
    )
