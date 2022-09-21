import subprocess

from commons.exceptions import BotError

def clone(url: str, path: str, base: str="git", **kwargs):
    subprocess.run([base, "clone", url, path], **kwargs).check_returncode()

def clone_no_checkout(url: str, path: str, base: str="git", **kwargs):
    subprocess.run([base, "clone", "--no-checkout", url, path], **kwargs).check_returncode()

def fetch(branch: str="main", base: str="git", **kwargs):
    subprocess.run([base, "fetch", "origin", branch], **kwargs).check_returncode()

def reset_soft(branch: str="main", base: str="git", **kwargs):
    subprocess.run([base, "reset", "--soft", branch], **kwargs).check_returncode()

def reset_hard(branch: str = "main", base: str = "git", **kwargs):
    subprocess.run([base, "reset", "--hard", branch], **kwargs).check_returncode()

def checkout_file(path: str, branch: str="main", base: str="git", **kwargs):
    subprocess.run([base, "checkout", f"origin/{branch}", "--", path], **kwargs).check_returncode()

def checkout(branch: str, base: str="git", **kwargs):
    subprocess.run([base, "checkout", "-B", branch], check=True, **kwargs)

def add(path: str, base: str="git", **kwargs):
    subprocess.run([base, "add", path], **kwargs).check_returncode()

def commit(message: str, base: str="git", **kwargs):
    subprocess.run([base, "commit", "-m", message], **kwargs).check_returncode()

def push(branch="main", base: str="git", **kwargs):
    subprocess.run([base, "push", "origin", branch], **kwargs).check_returncode()

def delete_branch(branch: str, base: str="git", **kwargs):
    subprocess.run([base, "push", "origin", "--delete", branch], check=True, **kwargs)

def remove(path: str, base: str="git", **kwargs):
    subprocess.run([base, "rm", path], **kwargs).check_returncode()

def restore_staged(path: str, base: str="git", **kwargs):
    subprocess.run([base, "restore", "--staged", path], **kwargs).check_returncode()

def file_version(path: str, base: str="git", **kwargs):
    if subprocess.run([base, "status", "--short", path], capture_output=True, encoding='utf-8', check=True).stdout.strip() != "":
        suffix = "-dirty"
    else:
        suffix = ""
    sp = subprocess.run([base, "log", "-n", "1", "--pretty=format:%h", "--", path], capture_output=True, encoding='utf-8', **kwargs)
    sp.check_returncode()
    return sp.stdout.strip() + suffix

def get_branch(base: str="git", **kwargs):
    return subprocess.run([base, "branch", "--show-current"], capture_output=True, encoding='utf-8', check=True, **kwargs).stdout.strip()