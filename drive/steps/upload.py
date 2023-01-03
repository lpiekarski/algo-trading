from core.drive import get_drive_module


def upload(local_path, remote_path, **kwargs):
    drive = get_drive_module()
    drive.upload(local_path, remote_path)
