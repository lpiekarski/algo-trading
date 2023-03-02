import logging

from core.data.utils import binary_crossentropy, accuracy, precision, negative_precision, recall, balanced_accuracy, \
    specificity, mcc
import core.data.utils as metric_source
import numpy as np

from core.drive_utils.models import download_model_config

LOGGER = logging.getLogger(__name__)


def evaluate_predictions(dataset, y_pred, label, model_config, **kwargs):
    LOGGER.info("Comparing predictions to labels")
    if label is None and len(dataset.labels) == 1:
        LOGGER.info(f"Dataset implied label '{dataset.labels[0]}'")
        label = dataset.labels[0]
    y_true = dataset.get_y(*label.split(",")).to_numpy().astype(np.float32)
    y_pred = np.array(y_pred).astype(np.float32)
    metrics = dict(
        binary_cross_entropy=binary_crossentropy,
        accuracy=accuracy,
        balanced_accuracy=balanced_accuracy,
        precision=precision,
        negative_precision=negative_precision,
        recall=recall,
        specificity=specificity,
        mcc=mcc
    )
    if model_config is not None:
        cfg = download_model_config(model_config)
        if "metrics" in cfg:
            metrics = {
                metric_name: getattr(metric_source, metric_fn)
                for metric_name, metric_fn in cfg["metrics"].items()
            }
    return dict(
        eval={
            metric_name: metric_fn(y_true, y_pred)
            for metric_name, metric_fn in metrics.items()
        }
    )
