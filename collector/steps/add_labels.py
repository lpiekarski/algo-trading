import logging
import yaml
import core.data.labels as ls

LOGGER = logging.getLogger(__name__)
DEFAULT_LABEL_CONFIG = dict(
    best_decision=[0.0025],
    price_direction=None,
    price_log_return=None
)


def add_labels(dataset, labels=None, **kwargs):
    label_config = None
    if labels is not None:
        with open(labels, 'r') as f:
            label_config = yaml.load(f, yaml.CLoader)
    if label_config is None:
        label_config = DEFAULT_LABEL_CONFIG
    for label, params in label_config.items():
        LOGGER.info(f"Adding label '{label}' with parameters: {params}")
        label_func = getattr(ls, label)
        if params is None:
            label_func(dataset)
        else:
            for param in params:
                if isinstance(param, list):
                    label_func(dataset, *param)
                elif isinstance(param, dict):
                    label_func(dataset, **param)
                else:
                    label_func(dataset, param)
