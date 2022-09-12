import logging
from commons.timing import step
from model import predictors

LOGGER = logging.getLogger(__name__)

@step
def get_model_module(model=None, *args, **kwargs):
    model_module = predictors.get_model_module(model)
    return dict(model_module=model_module)