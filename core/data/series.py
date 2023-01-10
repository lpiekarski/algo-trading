from numpy.lib.stride_tricks import sliding_window_view


def rolling_window(length, x, y=None):
    """
    Apply rolling window transformation
    :param length: length of the window
    :param x: input array of shape (num_observations, num_features)
    :param y: input array of shape (num_observations)
    :return: transformed arrays of shape (num_observations - length, num_features, length), (num_observations - length, length)
    """
    ret_x = sliding_window_view(x, window_shape=length, axis=0)
    if y is None:
        return ret_x
    ret_y = sliding_window_view(y, window_shape=length, axis=0)
    return ret_x, ret_y
