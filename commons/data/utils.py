import numpy as np


def log_change(series):
    return np.log(series / series.shift(1))
