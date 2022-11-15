from typing import Any

import pandas as pd
import numpy as np


def initialize(config_json: Any) -> None:
    pass


def predict(x: pd.DataFrame) -> np.ndarray:
    return np.ones_like(x["Close"])


def train(x: pd.DataFrame, y: pd.DataFrame) -> None:
    pass


def save_weights(path: str) -> None:
    pass


def load_weights(path: str) -> None:
    pass
