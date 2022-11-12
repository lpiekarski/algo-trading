import logging

from commons.timing import step

LOGGER = logging.getLogger(__name__)


def conditional(step_func, if_true, negation=False):
    def conditional_step(*args, **kwargs):
        if if_true not in kwargs or (
            if_true in kwargs and negation != bool(
                kwargs[if_true])):
            if hasattr(step_func, 'pure'):
                return getattr(step_func, 'pure')(*args, **kwargs)
            else:
                return step_func(*args, **kwargs)
        elif not hasattr(conditional_step, "invisible") or not conditional_step.invisible:
            LOGGER.info(f"Skipping.")

    conditional_step.__name__ = step_func.__name__
    conditional_step.pure = step_func
    if hasattr(step_func, "invisible"):
        conditional_step.invisible = step_func.invisible
    return step(conditional_step)
