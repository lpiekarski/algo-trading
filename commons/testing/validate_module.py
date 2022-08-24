from inspect import signature

def validate_shape(module, interface):
    for func_name in interface.keys():
        if not hasattr(module, func_name):
            raise AssertionError(f"Expected module {module.__name__} to have a function named '{func_name}' with interface {interface[func_name]}")
        sig = signature(getattr(module, func_name))
        func = interface[func_name]
        if sig.return_annotation != func["return_type"]:
            raise AssertionError(f"Expected {func_name} from module {module.__name__} to have return type '{func['return_type']}', but it has '{sig.return_annotation}'")
        expected_param_types = func["parameter_types"]
        i = 0
        for parameter in sig.parameters.values():
            if expected_param_types[i] != parameter.annotation:
                raise AssertionError(f"Expected {func_name} from module {module.__name__} to have parameter with type '{parameter.annotation}', but it has type '{expected_param_types[i]}'")
            i += 1