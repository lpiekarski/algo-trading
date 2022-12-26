import logging

from commons.data.utils import binary_crossentropy, accuracy, precision, recall
from commons.timing import step
import numpy as np

LOGGER = logging.getLogger(__name__)


@step
def evaluate_predictions(dataset, y_pred, label, **kwargs):
    LOGGER.info("Comparing predictions to labels")
    if label is None and len(dataset.labels) == 1:
        LOGGER.info(f"Dataset implied label '{dataset.labels[0]}'")
        label = dataset.labels[0]
    y_true = dataset.get_y(label).to_numpy().astype(np.float32)
    y_pred = np.array(y_pred).astype(np.float32)
    return dict(eval=dict(
        binary_cross_entropy=binary_crossentropy(y_true, y_pred),
        accuracy=accuracy(y_true, y_pred),
        precision=precision(y_true, y_pred),
        recall=recall(y_true, y_pred),
    ))
