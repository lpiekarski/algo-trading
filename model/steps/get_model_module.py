import logging
from model import predictors

LOGGER = logging.getLogger(__name__)


def get_model_module(model, **kwargs):
    model_module = predictors.get_model_module(model)
    return dict(model_module=model_module)
