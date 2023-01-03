import logging
from typing import Dict

from commons.subcommand_execution.step import Step, StepLogLevel

LOGGER = logging.getLogger(__name__)


class RenameParameters(Step):
    """
    RenameParameters step swaps names of the parameters.
    """

    def __init__(self, mapping: Dict[str, str], keep_old=False):
        super().__init__(f"rename parameters (keep_old={keep_old}) {mapping}", self.__module__, StepLogLevel.DEBUG)
        self.mapping = mapping
        self.keep_old = keep_old

    def callback(self, *args, **kwargs):
        inv_mapping = dict((v, kwargs[k]) if k in kwargs else (
            v, None) for k, v in self.mapping.items())
        if self.keep_old:
            for k, v in self.mapping.items():
                if k in kwargs:
                    inv_mapping[k] = kwargs[k]
        return inv_mapping
