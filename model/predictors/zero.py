import pandas as pd
import numpy as np


def predict(x: pd.DataFrame) -> np.ndarray:
    return np.zeros_like(x["Close"])


def train(x: pd.DataFrame, y: pd.DataFrame) -> None:
    pass


def save(path: str) -> None:
    pass


def load(path: str) -> None:
    pass
