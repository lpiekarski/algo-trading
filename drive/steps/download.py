from commons.drive import get_drive_module
from commons.timing import step

@step
def download(remote_path, local_path, **kwargs):
    drive = get_drive_module()
    drive.download(remote_path, local_path)
