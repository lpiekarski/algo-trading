from commons.drive import get_drive_module
from commons.timing import step

@step
def upload(local_path, remote_path, **kwargs):
    drive = get_drive_module()
    drive.upload(local_path, remote_path)
