from numpy.lib.stride_tricks import sliding_window_view


def convert_to_series(x, y, length):
    return sliding_window_view(x, window_shape=length), y[(length - 1):].copy()
