import subprocess
import logging

LOGGER = logging.getLogger(__name__)

def clone(url: str, path: str, base: str="git", **kwargs):
    cmd(base, "clone", url, path, **kwargs)

def clone_no_checkout(url: str, path: str, base: str="git", **kwargs):
    cmd(base, "clone", "--no-checkout", '--single-branch', url, path, **kwargs)

def fetch(branch: str="main", base: str="git", **kwargs):
    cmd(base, "fetch", "origin", branch, **kwargs)

def reset_soft(branch: str="main", base: str="git", **kwargs):
    cmd(base, "reset", "--soft", branch, **kwargs)

def reset_hard(branch: str = "main", base: str = "git", **kwargs):
    cmd(base, "reset", "--hard", branch, **kwargs)

def checkout_file(path: str, branch: str="main", base: str="git", **kwargs):
    cmd(base, "checkout", f"origin/{branch}", "--", path, **kwargs)

def checkout(branch: str, base: str="git", **kwargs):
    cmd(base, "remote", "set-branches", "origin", branch, **kwargs)
    cmd(base, "fetch", "origin", branch, **kwargs)
    cmd(base, "checkout", "-B", branch, **kwargs)

def checkout_create(branch: str, base: str="git", **kwargs):
    cmd(base, "checkout", "-B", branch, **kwargs)

def add(path: str, base: str="git", **kwargs):
    cmd(base, "add", path, **kwargs)

def commit(message: str, base: str="git", **kwargs):
    cmd(base, "commit", "-m", message, **kwargs)

def push(branch="main", base: str="git", **kwargs):
    cmd(base, "push", "origin", branch, **kwargs)

def delete_branch(branch: str, base: str="git", **kwargs):
    cmd(base, "push", "origin", "--delete", branch, **kwargs)

def remove(path: str, base: str="git", **kwargs):
    cmd(base, "rm", path, **kwargs)

def restore_staged(path: str, base: str="git", **kwargs):
    cmd(base, "restore", "--staged", path, **kwargs)

def file_version(path: str, base: str="git", **kwargs):
    if cmd(base, "status", "--short", path, **kwargs).strip() != "":
        suffix = "-dirty"
    else:
        suffix = ""
    return cmd(base, "log", "-n", "1", "--pretty=format:%h", "--", path, **kwargs).strip() + suffix

def get_branch(base: str="git", **kwargs):
    return cmd(base, "branch", "--show-current", **kwargs).strip()

def cmd(*args, **kwargs):
    LOGGER.debug(f"Running command ({kwargs}):\n{args}")
    sp = subprocess.run(args, capture_output=True, encoding='utf-8', **kwargs)
    output = sp.stdout
    LOGGER.debug(output)
    sp.check_returncode()
    return output
