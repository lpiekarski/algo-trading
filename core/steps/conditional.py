import logging

from core.subcommand_execution.step import Step, StepLogLevel

LOGGER = logging.getLogger(__name__)


class Conditional(Step):
    """
    Conditional step allows for executing certain part
    of the subcommand only if given flag is set to the specified value
    """

    def __init__(self, wrapped_step, flag_name: str, flag_value=True):
        super().__init__(
            f"({Step.get_name(wrapped_step)}) if{' not' if not flag_value else ''} '{flag_name}'",
            f"{self.__module__}->{Step.get_module(wrapped_step)}",
            StepLogLevel.INFO)
        self.wrapped_step = wrapped_step
        self.flag_name = flag_name
        self.flag_value = flag_value

    def callback(self, *args, **kwargs):
        if self.flag_name in kwargs:
            if kwargs[self.flag_name] == "True":
                flag_value = True
            elif kwargs[self.flag_name] == "False":
                flag_value = False
            else:
                flag_value = bool(kwargs[self.flag_name])
        else:
            flag_value = False
        if flag_value != self.flag_value:
            LOGGER.info("Skipping")
            return
        return self.wrapped_step(*args, **kwargs)
