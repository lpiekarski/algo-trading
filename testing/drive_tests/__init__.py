import filecmp
import logging
import os

from commons.env import getenv
from commons.import_utils import module_from_file
from commons.string import BREAK

LOGGER = logging.getLogger(__name__)

def run_drive_tests():
    LOGGER.info("")
    LOGGER.info(f'--- drive tests ---')
    cd = os.path.dirname(os.path.realpath(__file__))
    LOCAL_STORE = getenv("CACHE_DIR")
    root = os.path.join(cd, '..', '..', 'commons/drive')
    fail_cause = None
    test_filename = 'drive_test.txt'
    local_store_testfile = os.path.join(LOCAL_STORE, test_filename)
    resources_testfile = os.path.join(cd, '..', 'resources', test_filename)
    LOGGER.info(f'Paths:')
    LOGGER.info(f'Local store test file location: {os.path.abspath(local_store_testfile)}')
    LOGGER.info(f'Test file in resources: {os.path.abspath(resources_testfile)}')
    for file in os.listdir(root):
        try:
            if os.path.exists(local_store_testfile):
                os.remove(local_store_testfile)
            path = os.path.join(root, file)
            basename = os.path.basename(path)
            if not basename.startswith("__"):
                LOGGER.info(f"Testing drive module: {os.path.abspath(path)}")
                drive_module = module_from_file(path)
                LOGGER.info(f"\tUploading test file")
                drive_module.upload(resources_testfile, test_filename)
                LOGGER.info(f"\tDownloading test file")
                drive_module.download(test_filename, local_store_testfile)
                if not os.path.exists(local_store_testfile):
                    raise AssertionError(f"Drive module '{os.path.abspath(drive_module.__name__)}' failed to download test file")
                if not filecmp.cmp(resources_testfile, local_store_testfile):
                    raise AssertionError(f"Downloaded file is not the same as uploaded for drive '{os.path.abspath(drive_module.__name__)}'")
        except Exception as e:
            LOGGER.error(f"{e}", exc_info=e)
            if fail_cause is None:
                fail_cause = e
        finally:
            if os.path.exists(local_store_testfile):
                os.remove(local_store_testfile)
    if fail_cause is not None:
        raise AssertionError(fail_cause)