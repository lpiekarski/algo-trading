import pandas as pd
import numpy as np

def predict(X: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame()
    df["y"] = np.zeros_like(X["Close"])
    return df


def train(X: pd.DataFrame, y: pd.DataFrame) -> None:
    pass