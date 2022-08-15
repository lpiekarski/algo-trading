import importlib
import os
import click
import logging
import importlib.util
import sys
from commons.timing import command_success

__all__ = ["test", "test_group"]

from testing.validate_module import validate_shape

LOGGER = logging.getLogger(__name__)

@click.group()
def test_group():
    pass

@test_group.command()
def test():
    validate_module_shapes()
    command_success(LOGGER)

def validate_module_shapes():
    for root, _, files in os.walk(".", topdown=False):
        for name in files:
            if name == "__shapes__.py":
                shapes = module_from_file(os.path.join(root, name))
                interface = getattr(shapes, "interface")
                for file in os.listdir(root):
                    path = os.path.join(root, file)
                    basename = os.path.basename(path)
                    if not basename.startswith("__"):
                        LOGGER.info(f"Testing module constraints for: {path}")
                        module = module_from_file(path)
                        validate_shape(module, interface)

def module_from_file(path):
    spec = importlib.util.spec_from_file_location(str(path), path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[str(path)] = module
    spec.loader.exec_module(module)
    return module


if __name__ == '__main__':
    test()