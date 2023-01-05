import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score


def log(x, epsilon=1e-8):
    return np.log(x + epsilon)


def log_change(series):
    return log(series / series.shift(1))


def accuracy(y_pred, y_true):
    return accuracy_score(y_true.flatten().astype(np.uint8), np.round(y_pred.flatten()).astype(np.uint8))


def precision(y_pred, y_true):
    return precision_score(y_true.flatten().astype(np.uint8), np.round(y_pred.flatten()).astype(np.uint8))


def recall(y_pred, y_true):
    return recall_score(y_true.flatten().astype(np.uint8), np.round(y_pred.flatten()).astype(np.uint8))


def binary_crossentropy(y_true, y_pred):
    y_true = y_true.flatten()
    y_pred = y_pred.flatten()
    return np.sum(- y_true * log(y_pred) - (1 - y_true)
                  * log(1 - y_pred)) / y_true.shape[0]
