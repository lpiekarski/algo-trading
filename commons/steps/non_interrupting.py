import logging

from commons.exceptions import NonInterruptingError
from commons.subcommand_execution.step import Step, StepLogLevel

LOGGER = logging.getLogger(__name__)


class NonInterrupting(Step):
    """
    Non-interrupting step prevents any exception thrown by the wrapped step to stop the execution of the subcommand
    by converting the exception to NonInterruptingError.
    """

    def __init__(self, wrapped_step):
        super().__init__(f"(not interrupting {Step.get_name(wrapped_step)})", self.__module__, StepLogLevel.INFO)
        self.wrapped_step = wrapped_step

    def callback(self, *args, **kwargs):
        try:
            self.wrapped_step(*args, **kwargs)
        except Exception as e:
            raise NonInterruptingError(e)
