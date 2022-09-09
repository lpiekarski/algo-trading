import pandas as pd


def predict(X: pd.DataFrame) -> pd.DataFrame:
    res = pd.DataFrame()
    res['y_pred'] = X["Open"]
    return res


def train(X: pd.DataFrame, y: pd.DataFrame) -> None:
    pass