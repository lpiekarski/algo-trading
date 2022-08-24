import filecmp
import logging
import os

from commons.import_utils import module_from_file
from commons.string import BREAK

LOGGER = logging.getLogger(__name__)

def run_drive_tests():
    LOGGER.info(f'{BREAK}')
    LOGGER.info(f'Running drive tests')
    LOGGER.info(f'{BREAK}')
    root = 'commons/drive'
    fail_cause = None
    for file in os.listdir(root):
        try:
            if os.path.exists('data/drive_test.txt'):
                os.remove('data/drive_test.txt')
            path = os.path.join(root, file)
            basename = os.path.basename(path)
            if not basename.startswith("__"):
                LOGGER.info(f"Testing drive module: {path}")
                drive_module = module_from_file(path)
                LOGGER.info(f"\tUploading test file")
                drive_module.upload('testing/resources/drive_test.txt', 'drive_test.txt')
                LOGGER.info(f"\tDownloading test file")
                drive_module.download('drive_test.txt', 'data/drive_test.txt')
                if not os.path.exists('data/drive_test.txt'):
                    raise AssertionError(f"Drive module '{drive_module.__name__}' failed to download test file")
                if not filecmp.cmp('testing/resources/drive_test.txt', 'data/drive_test.txt'):
                    raise AssertionError(f"Downloaded file is not the same as uploaded for drive '{drive_module.__name__}'")
        except AssertionError as e:
            LOGGER.error(f"{e}")
            if fail_cause is None:
                fail_cause = e
        finally:
            if os.path.exists('data/drive_test.txt'):
                os.remove('data/drive_test.txt')
    if fail_cause is not None:
        raise AssertionError(fail_cause)