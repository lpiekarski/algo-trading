import logging
import os

from commons.import_utils import module_from_file
from commons.timing import run_step
from testing.shape_tests.validate_module import validate_shape

LOGGER = logging.getLogger(__name__)

@run_step
def shape_tests(skip_shapes=False, *args, **kwargs):
    if skip_shapes:
        LOGGER.info("Tests are skipped.")
        return
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