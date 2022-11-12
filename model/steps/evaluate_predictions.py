import logging
from commons.timing import step
import numpy as np
from sklearn.metrics import accuracy_score

LOGGER = logging.getLogger(__name__)


def log(x, epsilon=1e-8):
    return np.log(x + epsilon)


def binary_logloss(y_true, y_pred):
    return np.sum(- y_true * log(y_pred) - (1 - y_true)
                  * log(1 - y_pred)) / y_true.shape[0]


@step
def evaluate_predictions(dataset, y_pred, label, **kwargs):
    LOGGER.info("Comparing predictions to labels")
    if label is None and len(dataset.labels) == 1:
        LOGGER.info(f"Dataset implied label '{dataset.labels[0]}'")
        label = dataset.labels[0]
    y_true = dataset.get_y(label).to_numpy().astype(np.float32)
    y_pred = np.array(y_pred).astype(np.float32)
    binary_cross_entropy = binary_logloss(y_true, y_pred)
    accuracy = accuracy_score(y_true, np.round(y_pred))
    return dict(binary_cross_entropy=binary_cross_entropy, accuracy=accuracy)
