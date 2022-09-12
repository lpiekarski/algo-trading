import pandas as pd
import numpy as np

def predict(X: pd.DataFrame) -> pd.DataFrame:
    res = pd.DataFrame()
    res['y_pred'] = np.zeros_like(X["Close"])
    return res

def train(X: pd.DataFrame, y: pd.DataFrame) -> None:
    pass