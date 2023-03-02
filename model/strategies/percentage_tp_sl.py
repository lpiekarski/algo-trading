from typing import List
import pandas as pd
import numpy as np

from trader.broker_apis import Signal, Trade

threshold: float = 0
volume: float = 0.01
tpsl_pct: float = 0.01
enable_long_positions: bool = True
enable_short_positions: bool = True


def initialize(config_dict: dict | None = None):
    global threshold
    global volume
    global tpsl_pct
    global enable_long_positions
    global enable_short_positions
    if config_dict is not None:
        if "threshold" in config_dict:
            threshold = config_dict["threshold"]
        if "volume" in config_dict:
            volume = config_dict["volume"]
        if "tpsl_pct" in config_dict:
            tpsl_pct = config_dict["tpsl_pct"]
        if "enable_long_positions" in config_dict:
            enable_long_positions = config_dict["enable_long_positions"]
        if "enable_short_positions" in config_dict:
            enable_short_positions = config_dict["enable_short_positions"]


def load_state(path: str):
    pass


def get_trades(predictions: np.ndarray, data: pd.DataFrame) -> List[Trade]:
    predictions = predictions.squeeze()
    if len(predictions.shape) == 1:
        signals = np.full_like(predictions, Signal.NO_ACTION)
        if enable_long_positions:
            signals[predictions > 0.5 + threshold] = Signal.BUY
        if enable_short_positions:
            signals[predictions < 0.5 - threshold] = Signal.SELL
    else:
        choice = np.argmax(predictions, axis=1)
        signals = np.full((predictions.shape[0],), Signal.NO_ACTION)
        if enable_long_positions:
            signals[(choice == 0) & (predictions[:, 0] > threshold)] = Signal.BUY
        if enable_short_positions:
            signals[(choice == 1) & (predictions[:, 1] > threshold)] = Signal.SELL
    return [
        Trade(
            signal,
            price,
            volume,
            *swap_if_short(price * (1 + tpsl_pct), price * (1 - tpsl_pct), signal),
            comment=f"Prediction: {predictions[idx]}"
        ) for idx, (signal, price) in enumerate(zip(signals, data["Close"]))
    ]


def save_state(path: str):
    pass


def swap_if_short(x, y, signal):
    return (y, x) if signal == Signal.SELL else (x, y)
