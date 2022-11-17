import numpy as np


def log_change(series):
    return np.log(series / series.shift(1))


def accuracy(y_pred, y_true):
    return (np.round(y_pred) == y_true).sum() / len(y_true)
