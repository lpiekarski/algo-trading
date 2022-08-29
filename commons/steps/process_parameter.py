import logging

from commons.env import getenv
from commons.exceptions import ArgumentError
from commons.timing import run_step

LOGGER = logging.getLogger(__name__)

def process_parameter(param_name: str, optional=False):
    def process_parameter_step(*args, **kwargs):
        if kwargs[param_name] is None:
            param_value = getenv(param_name)
            if param_value is None:
                if optional:
                    LOGGER.warning(f"'{param_name}' is not set.")
                else:
                    raise ArgumentError(f"Provide --{param_name} option or set it through an environment variable '{param_name}'")
            return {param_name: param_value}

    process_parameter_step.__name__ = f"process_'{param_name}'_parameter"
    return run_step(process_parameter_step)