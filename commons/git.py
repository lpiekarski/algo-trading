import subprocess

from commons.exceptions import BotError

def clone(url: str, path: str, base: str="git", **kwargs):
    subprocess.run([base, "clone", url, path], **kwargs).check_returncode()

def clone_no_checkout(url: str, path: str, base: str="git", **kwargs):
    subprocess.run([base, "clone", "--no-checkout", url, path], **kwargs).check_returncode()

def fetch(base: str="git", **kwargs):
    subprocess.run([base, "fetch", "origin", "main"], **kwargs).check_returncode()

def reset_soft(base: str="git", **kwargs):
    subprocess.run([base, "reset", "--soft", "main"], **kwargs).check_returncode()

def checkout(path: str, base: str="git", **kwargs):
    subprocess.run([base, "checkout", "origin/main", "--", path], **kwargs).check_returncode()

def add(path: str, base: str="git", **kwargs):
    subprocess.run([base, "add", path], **kwargs).check_returncode()

def commit(message: str, base: str="git", **kwargs):
    subprocess.run([base, "commit", "-m", message], **kwargs).check_returncode()

def push(base: str="git", branch="main", **kwargs):
    subprocess.run([base, "push", "origin", branch], **kwargs).check_returncode()

def remove(path: str, base: str="git", **kwargs):
    subprocess.run([base, "rm", path], **kwargs).check_returncode()

def restore_staged(path: str, base: str="git", **kwargs):
    subprocess.run([base, "restore", "--staged", path], **kwargs).check_returncode()

def file_version(path: str, base: str="git", **kwargs):
    if subprocess.run([base, "status", "--short", path], capture_output=True, encoding='utf-8', check=True).stdout.strip() != "":
        raise BotError(f"File '{path}' has been modified. Commit or revert the changes.")
    sp = subprocess.run([base, "log", "-n", "1", "--pretty=format:%h", "--", path], capture_output=True, encoding='utf-8', **kwargs)
    sp.check_returncode()
    return sp.stdout.strip()

def get_branch(base: str="git", **kwargs):
    return subprocess.run([base, "branch", "--show-current"], capture_output=True, encoding='utf-8', check=True, **kwargs).stdout.strip()