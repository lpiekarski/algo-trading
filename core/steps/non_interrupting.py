import logging

from core.exceptions import NonInterruptingError
from core.subcommand_execution.step import Step, StepLogLevel

LOGGER = logging.getLogger(__name__)


class NonInterrupting(Step):
    """
    Non-interrupting step prevents any exception thrown by the wrapped step to stop the execution of the subcommand
    by converting the exception to NonInterruptingError.
    """

    def __init__(self, wrapped_step):
        super().__init__(f"non-interrupting ({Step.get_name(wrapped_step)})", self.__module__, StepLogLevel.INFO)
        self.wrapped_step = wrapped_step

    def callback(self, *args, **kwargs):
        try:
            return self.wrapped_step(*args, **kwargs)
        except Exception as e:
            raise NonInterruptingError(e)
