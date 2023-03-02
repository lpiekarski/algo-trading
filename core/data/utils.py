import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, balanced_accuracy_score, matthews_corrcoef


def log(x, epsilon=1e-8):
    return np.log(x + epsilon)


def log_change(series, offset=1):
    values = np.array(series[:-offset])
    values_shifted = np.array(series[offset:])
    result = log(values_shifted / values)
    if len(result.shape) == 2:
        return np.concatenate([[np.full((result.shape[1],), np.nan) for _ in range(offset)], result], axis=0)
    return np.concatenate([[np.nan for _ in range(offset)], result], axis=0)


def accuracy(y_true, y_pred):
    y_true = round_(y_true)
    y_pred = round_(y_pred)
    return accuracy_score(y_true, y_pred)


def winrate(y_true, y_pred, threshold):
    choice_gt = np.argmax(y_true, axis=1)
    choice = np.argmax(y_pred, axis=1)
    choice[(choice == 0) & (y_pred[:, 0] < threshold)] = 2
    choice[(choice == 1) & (y_pred[:, 1] < threshold)] = 2
    wr_buy = (choice == 0) & (choice_gt == 0)
    wr_sell = (choice == 1) & (choice_gt == 1)
    return (wr_buy | wr_sell).sum() / (((choice == 0) | (choice == 1)).sum() + 1e-8)


def winrate_3(y_true, y_pred):
    return winrate(y_true, y_pred, 0.3)


def winrate_4(y_true, y_pred):
    return winrate(y_true, y_pred, 0.4)


def winrate_5(y_true, y_pred):
    return winrate(y_true, y_pred, 0.5)


def winrate_6(y_true, y_pred):
    return winrate(y_true, y_pred, 0.6)


def winrate_7(y_true, y_pred):
    return winrate(y_true, y_pred, 0.7)


def winrate_8(y_true, y_pred):
    return winrate(y_true, y_pred, 0.8)


def winrate_9(y_true, y_pred):
    return winrate(y_true, y_pred, 0.3)


def balanced_accuracy(y_true, y_pred):
    y_true = round_(y_true)
    y_pred = round_(y_pred)
    return balanced_accuracy_score(y_true, y_pred)


def multiclass_balanced_accuracy(y_true, y_pred):
    y_true = np.argmax(y_true, axis=1)
    y_pred = np.argmax(y_pred, axis=1)
    return balanced_accuracy_score(y_true, y_pred)


def class1_frequency(y_true, y_pred):
    return (np.argmax(y_pred, axis=1) == 0).mean()


def class2_frequency(y_true, y_pred):
    return (np.argmax(y_pred, axis=1) == 1).mean()


def class3_frequency(y_true, y_pred):
    return (np.argmax(y_pred, axis=1) == 2).mean()


def precision(y_true, y_pred):
    y_true = round_(y_true)
    y_pred = round_(y_pred)
    return precision_score(y_true, y_pred, zero_division=0)


def negative_precision(y_true, y_pred):
    y_true = round_(y_true)
    y_pred = round_(y_pred)
    return precision_score(y_true, y_pred, zero_division=0, pos_label=0)


def recall(y_true, y_pred):
    y_true = round_(y_true)
    y_pred = round_(y_pred)
    return recall_score(y_true, y_pred, zero_division=0)


def specificity(y_true, y_pred):
    y_true = round_(y_true)
    y_pred = round_(y_pred)
    return recall_score(y_true, y_pred, zero_division=0, pos_label=0)


def mcc(y_true, y_pred):
    y_true = round_(y_true)
    y_pred = round_(y_pred)
    return matthews_corrcoef(y_true, y_pred)


def binary_crossentropy(y_true, y_pred):
    y_true = y_true.flatten()
    y_pred = y_pred.flatten()
    return np.sum(- y_true * log(y_pred) - (1 - y_true)
                  * log(1 - y_pred)) / y_true.shape[0]


def round_(arr):
    ret = np.zeros_like(arr)
    ret[arr > 0.5] = 1
    ret[arr < 0.5] = 0
    return ret.astype(np.uint8)


def winrate_1d(y_true, y_pred, threshold):
    choice_gt = (y_true > 0.5).astype(np.uint8)
    choice = (y_pred > 0.5).astype(np.uint8)
    choice[np.abs(y_pred - 0.5) < threshold] = 2
    wr_buy = (choice == 0) & (choice_gt == 0)
    wr_sell = (choice == 1) & (choice_gt == 1)
    return (wr_buy | wr_sell).sum() / (((choice == 0) | (choice == 1)).sum() + 1e-8)


def winrate_1d_0(y_true, y_pred):
    return winrate_1d(y_true, y_pred, 0)


def winrate_1d_01(y_true, y_pred):
    return winrate_1d(y_true, y_pred, 0.01)


def winrate_1d_05(y_true, y_pred):
    return winrate_1d(y_true, y_pred, 0.05)


def winrate_1d_1(y_true, y_pred):
    return winrate_1d(y_true, y_pred, 0.1)


def profit_1d(y_true, y_pred, threshold):
    y_pred = y_pred.squeeze()
    y_true = y_true.squeeze()
    choice_gt = (y_true > 0.5).astype(np.uint8)
    choice = (y_pred > 0.5).astype(np.uint8)
    choice[np.abs(y_pred - 0.5) < threshold] = 2
    won_buys = ((choice == 0) & (choice_gt == 0)).sum()
    lost_buys = (choice == 1).sum() - won_buys
    won_sells = ((choice == 1) & (choice_gt == 1)).sum()
    lost_sells = (choice == 0).sum() - won_sells
    profit = (won_sells + won_buys) * (0.05 - 0.0015) - (lost_sells + lost_buys) * (0.05 + 0.0015)
    return profit


def profit_1d_0(y_true, y_pred):
    return profit_1d(y_true, y_pred, 0)


def profit_1d_01(y_true, y_pred):
    return profit_1d(y_true, y_pred, 0.01)


def profit_1d_05(y_true, y_pred):
    return profit_1d(y_true, y_pred, 0.05)


def profit_1d_1(y_true, y_pred):
    return profit_1d(y_true, y_pred, 0.1)
