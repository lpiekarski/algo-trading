from commons import drive_utils
from commons.timing import step

@step
def copy(source_path, target_path, **kwargs):
    drive_utils.copy_file(source_path, target_path)
