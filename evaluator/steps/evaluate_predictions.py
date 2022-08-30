import logging
import tensorflow as tf
from commons.timing import step

LOGGER = logging.getLogger(__name__)

@step
def evaluate_predictions(y=None, y_pred=None, *args, **kwargs):
    LOGGER.info("Comparing predictions to labels")
    cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=False)
    binary_cross_entropy = cross_entropy(y, y_pred).numpy()
    return dict(binary_cross_entropy=binary_cross_entropy)
