import pandas as pd
import numpy as np

def predict(X: pd.DataFrame) -> np.ndarray:
    return np.zeros_like(X["Close"])

def train(X: pd.DataFrame, y: pd.DataFrame) -> None:
    pass

def save(path: str) -> None:
    pass

def load(path: str) -> None:
    pass