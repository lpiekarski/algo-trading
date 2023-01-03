from commons.drive import get_drive_module


def download(remote_path, local_path, **kwargs):
    drive = get_drive_module()
    drive.download(remote_path, local_path)
