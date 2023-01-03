import logging
import os

from commons.subcommand_execution.step import StepLogLevel, Step

LOGGER = logging.getLogger(__name__)


class ProcessParameter(Step):
    """
    This step tries to retrieve a parameter value from environmental
    variable if it's not already set through other means.
    """

    def __init__(self, param_name: str):
        super().__init__(f"process parameter '{param_name}'", self.__module__, StepLogLevel.DEBUG)
        self.param_name = param_name

    def callback(self, *args, **kwargs):
        if self.param_name not in kwargs or kwargs[self.param_name] is None:
            param_value = os.getenv(self.param_name)
            if param_value is None:
                LOGGER.debug(f"'{self.param_name}' is not set.")
            else:
                LOGGER.debug(f"'{self.param_name} is set to '{param_value}'.")
            return {self.param_name: param_value}
        LOGGER.debug(f"'{self.param_name}' has value '{kwargs[self.param_name]}'.")
