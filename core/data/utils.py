import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, balanced_accuracy_score


def log(x, epsilon=1e-8):
    return np.log(x + epsilon)


def log_change(series):
    return log(series / series.shift(1))


def accuracy(y_true, y_pred):
    y_true = y_true.flatten().astype(np.uint8)
    y_pred = np.round(y_pred.flatten()).astype(np.uint8)
    return accuracy_score(y_true, y_pred)


def balanced_accuracy(y_true, y_pred):
    y_true = y_true.flatten().astype(np.uint8)
    y_pred = np.round(y_pred.flatten()).astype(np.uint8)
    return balanced_accuracy_score(y_true, y_pred)


def precision(y_true, y_pred):
    return precision_score(
        y_true.flatten().astype(
            np.uint8), np.round(
            y_pred.flatten()).astype(
                np.uint8), zero_division=0)


def recall(y_true, y_pred):
    return recall_score(y_true.flatten().astype(np.uint8), np.round(y_pred.flatten()).astype(np.uint8), zero_division=0)


def binary_crossentropy(y_true, y_pred):
    y_true = y_true.flatten()
    y_pred = y_pred.flatten()
    return np.sum(- y_true * log(y_pred) - (1 - y_true)
                  * log(1 - y_pred)) / y_true.shape[0]
