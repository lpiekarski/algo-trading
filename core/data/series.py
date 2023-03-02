import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


def rolling_window(length, x: np.ndarray, y=None, inter=None):
    """
    Apply rolling window transformation
    :param length: length of the window
    :param x: input array of shape (num_observations, num_features)
    :param y: input array of shape (num_observations)
    :return: transformed arrays of shape (num_observations - length, num_features, length), (num_observations - length, length)
    """
    if length >= x.shape[0]:
        if y is None:
            return np.array([x.T])
        return np.array([x.T]), np.array([y])
    if inter is None:
        inter = length // 2
    ret_x = sliding_window_view(x, window_shape=length, axis=0)[::inter]
    if y is None:
        return ret_x
    ret_y = sliding_window_view(y, window_shape=length, axis=0)[::inter]
    return ret_x, ret_y
