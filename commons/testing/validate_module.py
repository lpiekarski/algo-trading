from inspect import signature
from typing import Any


def validate_shape(module, interface):
    for func_name in interface.keys():
        if not hasattr(module, func_name):
            raise AssertionError(
                f"Expected module {module.__name__} to have a function named '{func_name}' with interface {interface[func_name]}")
        sig = signature(getattr(module, func_name))
        func = interface[func_name]
        if not is_subtype(sig.return_annotation, func["return_type"]):
            raise AssertionError(
                f"Expected {func_name} from module {module.__name__} to have return type '{func['return_type']}', but it has '{sig.return_annotation}'")
        expected_param_types = func["parameter_types"]
        i = 0
        for parameter in sig.parameters.values():
            if not is_subtype(parameter.annotation, expected_param_types[i]):
                raise AssertionError(
                    f"Expected {func_name} from module {module.__name__} to have parameter with type '{expected_param_types[i]}', but it has type '{parameter.annotation}'")
            i += 1


def is_subtype(t1, t2):
    if t2 is Any:
        return True
    elif t1 is t2:
        return True
    elif t1 == t2:
        return True
    elif isinstance(t1, type) and isinstance(t2, type):
        return t1 is t2
    elif isinstance(t1, type) or isinstance(t2, type):
        return False
    elif t1 is None:
        return t2 is None
    else:
        return issubclass(t1, t2)
