from commons.drive import get_drive_module
from commons.timing import step

@step
def delete(remote_path):
    drive = get_drive_module()
    drive.delete(remote_path)
