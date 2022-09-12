import pandas as pd
import numpy as np

def predict(X: pd.DataFrame) -> pd.DataFrame:
    res = pd.DataFrame()
    res['y_pred'] = np.random.random(X.shape[0])
    return res

def train(X: pd.DataFrame, y: pd.DataFrame) -> None:
    pass

def save(path: str) -> None:
    pass

def load(path: str) -> None:
    pass