import logging

from commons.timing import step

LOGGER = logging.getLogger(__name__)

def rename_parameters(mapping, keep_old=False):
    def rename_parameter_step(*args, **kwargs):
        inv_mapping = dict((v, kwargs[k]) if k in kwargs else (v, None) for k, v in mapping.items())
        if keep_old:
            for k, v in mapping.items():
                if k in kwargs:
                    inv_mapping[k] = kwargs[k]
        return inv_mapping

    rename_parameter_step.__name__ = f"rename_parameters"
    rename_parameter_step.invisible = True
    return step(rename_parameter_step)