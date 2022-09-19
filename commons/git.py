import subprocess

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