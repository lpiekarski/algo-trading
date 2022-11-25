import logging
import os

from commons.configparams import Config

LOGGER = logging.getLogger(__name__)


def get_cache_dir(drive_type):
    cache_base_dir = Config.require_param('CACHE_DIR')
    return os.path.join(
        cache_base_dir, f'{drive_type}', 'files'), os.path.join(
        cache_base_dir, f'{drive_type}', 'md5')
