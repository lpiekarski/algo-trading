from commons.env import require_env

def split_pathname(pathname):
    if ':' in pathname:
        drive, name = pathname.split(':', maxsplit=2)
        if name.startswith('/'):
            name = name[1:]
        return drive, name
    else:
        return require_env('drive'), pathname