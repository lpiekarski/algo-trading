import logging
import os
from commons.exceptions import ArgumentError
from commons.timing import step

LOGGER = logging.getLogger(__name__)


def process_parameter(param_name: str, optional=False):
    def process_parameter_step(*args, **kwargs):
        if param_name not in kwargs or kwargs[param_name] is None:
            param_value = os.getenv(param_name)
            if param_value is None:
                if optional:
                    LOGGER.debug(f"'{param_name}' is not set.")
                else:
                    raise ArgumentError(
                        f"Provide --{param_name} option or set it through an environment variable '{param_name}'.")
            LOGGER.debug(f"'{param_name} is set to '{param_value}'.")
            return {param_name: param_value}
        LOGGER.debug(f"'{param_name}' has value '{kwargs[param_name]}'.")

    process_parameter_step.__name__ = f"process_'{param_name}'_parameter"
    process_parameter_step.invisible = True
    return step(process_parameter_step)
