from typing import List
import pandas as pd
import numpy as np

from trader.broker_apis import Signal, Trade

threshold: float = 0
volume: float = 0.01
duration: float = 0.01


def initialize(config_dict: dict | None = None):
    global threshold
    global volume
    global duration
    if config_dict is not None:
        if "threshold" in config_dict:
            threshold = config_dict["threshold"]
        if "volume" in config_dict:
            volume = config_dict["volume"]
        if "duration" in config_dict:
            duration = config_dict["duration"]


def load_state(path: str):
    pass


def get_trades(predictions: np.ndarray, data: pd.DataFrame) -> List[Trade]:
    signals = np.full_like(predictions, Signal.NO_ACTION)
    signals[predictions > 0.5 + threshold] = Signal.BUY
    signals[predictions < 0.5 - threshold] = Signal.SELL
    return [Trade(signal, price, volume, close_after=duration) for
            signal, price in zip(signals, data["Close"])]


def save_state(path: str):
    pass
