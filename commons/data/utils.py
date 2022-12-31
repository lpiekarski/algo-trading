import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score


def log(x, epsilon=1e-8):
    return np.log(x + epsilon)


def log_change(series):
    return log(series / series.shift(1))


def accuracy(y_pred, y_true):
    return accuracy_score(y_true, np.round(y_pred))


def precision(y_pred, y_true):
    return precision_score(y_true, np.round(y_pred))


def recall(y_pred, y_true):
    return recall_score(y_true, np.round(y_pred))


def binary_crossentropy(y_true, y_pred):
    return np.sum(- y_true * log(y_pred) - (1 - y_true)
                  * log(1 - y_pred)) / y_true.shape[0]
