from core.data.dataset import Dataset
from core.data.labels.utils import get_weighted_best_decision
import numpy as np

from core.data.utils import log_change


def best_decision(dataset: Dataset, pct_change: float = 0.0025, smooth: bool = False, smoothing_number: int = 60):
    decision = get_weighted_best_decision(dataset, pct_change, smoothing_number)
    if not smooth:
        mask = decision != 0.5
        decision[mask] = np.round(decision[mask])
    dataset.add_label(f"Best_decision_{pct_change}{('_smooth_' + str(smoothing_number)) if smooth else ''}", decision)


def best_decision_buy_sell_hold(
        dataset: Dataset,
        pct_change: float = 0.0025,
        smooth: bool = False,
        smoothing_number: int = 60):
    decision = get_weighted_best_decision(dataset, pct_change, smoothing_number)
    mask_buy = decision > 0.5
    mask_sell = decision < 0.5
    mask_hold = decision == 0.5
    best_decision_buy = np.zeros_like(decision)
    best_decision_sell = np.zeros_like(decision)
    best_decision_hold = np.zeros_like(decision)
    if smooth:
        best_decision_buy = decision
        best_decision_sell = 1 - decision
        best_decision_hold[mask_hold] = 1
        best_decision_buy[mask_hold] = 0
        best_decision_sell[mask_hold] = 0
    else:
        best_decision_buy[mask_buy] = 1
        best_decision_sell[mask_sell] = 1
        best_decision_hold[mask_hold] = 1
    dataset.add_label(
        f"Best_decision_buy_{pct_change}{('_smooth_' + str(smoothing_number)) if smooth else ''}",
        best_decision_buy)
    dataset.add_label(
        f"Best_decision_sell_{pct_change}{('_smooth_' + str(smoothing_number)) if smooth else ''}",
        best_decision_sell)
    dataset.add_label(
        f"Best_decision_hold_{pct_change}{('_smooth_' + str(smoothing_number)) if smooth else ''}",
        best_decision_hold)


def price_direction(dataset: Dataset, offset: int = 1):
    prices = dataset.df["Close"][:-offset].to_numpy()
    next_prices = dataset.df["Close"][offset:].to_numpy()
    going_up = (next_prices > prices).astype(np.float32)
    going_up[next_prices == prices] = np.nan
    going_up = np.concatenate([going_up, [np.nan for _ in range(offset)]], axis=0)
    dataset.add_label(f"Price_direction_{offset}", going_up)


def price_log_return(dataset: Dataset, offset: int = 1):
    log_return = log_change(dataset.df["Close"], offset)
    log_return = np.roll(log_return, -offset)
    dataset.add_label(f"Price_log_return_{offset}", log_return)
