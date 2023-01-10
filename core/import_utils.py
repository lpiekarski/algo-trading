import importlib
import sys


def module_from_file(path):
    spec = importlib.util.spec_from_file_location(str(path), path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[str(path)] = module
    spec.loader.exec_module(module)
    return module
