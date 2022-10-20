import logging
from commons.timing import step
import numpy as np
from sklearn.metrics import accuracy_score, log_loss

LOGGER = logging.getLogger(__name__)

@step
def evaluate_predictions(dataset, y_pred, label, **kwargs):
    LOGGER.info("Comparing predictions to labels")
    y = dataset.get_y(label)
    binary_cross_entropy = log_loss(y, y_pred)
    accuracy = accuracy_score(y, np.round(y_pred))
    return dict(binary_cross_entropy=binary_cross_entropy, accuracy=accuracy)