import pandas as pd


def dataframe_no_empty_cols(df: pd.DataFrame):
    df_dropped = df.dropna(axis=1, how='all')
    if df_dropped.shape[1] != df.shape[1]:
        raise AssertionError(
            f"Empty columns in dataframe: {list(set(df.columns.to_list()) - set(df_dropped.columns.to_list()))}")
