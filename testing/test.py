import os
import click
import logging
from commons.import_utils import module_from_file
from commons.timing import command_success

__all__ = ["test", "test_group"]

from testing.validate_module import validate_shape

LOGGER = logging.getLogger(__name__)

@click.group()
def test_group():
    pass

@test_group.command()
@click.option("--skip_shapes", "-s", is_flag=True)
def test(skip_shapes: bool):
    if not skip_shapes:
        validate_module_shapes()
    command_success(LOGGER)

def validate_module_shapes():
    for root, _, files in os.walk(".", topdown=False):
        for name in files:
            if name == "__shapes__.py":
                shapes = module_from_file(os.path.join(root, name))
                interface = getattr(shapes, "interface")
                LOGGER.debug(f"Validating modules '{root}', expected interface:\n{interface}")
                for file in os.listdir(root):
                    path = os.path.join(root, file)
                    basename = os.path.basename(path)
                    if not basename.startswith("__"):
                        LOGGER.info(f"Testing module constraints for: {path}")
                        module = module_from_file(path)
                        validate_shape(module, interface)

if __name__ == '__main__':
    test()