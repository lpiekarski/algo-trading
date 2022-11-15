import logging

from commons.exceptions import NotInterruptingError
from commons.timing import step

LOGGER = logging.getLogger(__name__)


def not_interrupting(step_func):
    def not_interrupting_step(*args, **kwargs):
        try:
            if hasattr(step_func, 'pure'):
                return getattr(step_func, 'pure')(*args, **kwargs)
            else:
                return step_func(*args, **kwargs)
        except Exception as e:
            raise NotInterruptingError(e)

    not_interrupting_step.__name__ = step_func.__name__
    not_interrupting_step.pure = step_func
    if hasattr(step_func, "invisible"):
        not_interrupting_step.invisible = step_func.invisible
    return step(not_interrupting_step)
