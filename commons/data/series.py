from numpy.lib.stride_tricks import sliding_window_view


def rolling_window(length, x, y=None):
    ret_x = sliding_window_view(x, window_shape=length)
    if y is not None:
        return ret_x, y[(length - 1):].copy()
    else:
        return ret_x
