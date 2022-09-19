import logging
import tensorflow as tf
from commons.timing import step
import numpy as np

LOGGER = logging.getLogger(__name__)

@step
def evaluate_predictions(y=None, y_pred=None, *args, **kwargs):
    LOGGER.info("Comparing predictions to labels")
    cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=False)
    batch_size = 1024
    p_y = tf.keras.utils.pad_sequences(list(chunks(np.asarray(y, dtype=np.float32), batch_size)), batch_size, dtype=np.float32)
    p_y_pred = tf.keras.utils.pad_sequences(list(chunks(np.asarray(y_pred, dtype=np.float32), batch_size)), batch_size, dtype=np.float32)
    binary_cross_entropy = cross_entropy(p_y, p_y_pred).numpy()
    return dict(binary_cross_entropy=binary_cross_entropy)

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]