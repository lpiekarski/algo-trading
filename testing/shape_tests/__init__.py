import logging
import os

from commons.import_utils import module_from_file
from commons.string import BREAK
from commons.timing import start_step, step_success
from testing.shape_tests.validate_module import validate_shape

LOGGER = logging.getLogger(__name__)

def run_shape_tests():
    start_step(LOGGER, 'shape tests')
    cd = os.path.dirname(os.path.realpath(__file__))
    for root, _, files in os.walk(os.path.join(cd, '..', '..'), topdown=False):
        for name in files:
            if name == "__shapes__.py":
                shapes = module_from_file(os.path.join(root, name))
                interface = getattr(shapes, "interface")
                LOGGER.debug(f"Validating modules '{os.path.abspath(root)}', expected interface:\n{interface}")
                for file in os.listdir(root):
                    path = os.path.join(root, file)
                    basename = os.path.basename(path)
                    if not basename.startswith("__"):
                        LOGGER.info(f"Testing module constraints for: {os.path.abspath(path)}")
                        module = module_from_file(path)
                        validate_shape(module, interface)
                        LOGGER.info(f"\tModule '{os.path.abspath(module.__name__)}' is valid")
    step_success('shape tests')