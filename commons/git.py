import subprocess

def clone(url: str, path: str, base: str="git", **kwargs):
    subprocess.run([base, "clone", url, path], **kwargs).check_returncode()

def bare_clone(url: str, path: str, base: str="git", **kwargs):
    subprocess.run([base, "clone", "--filter=blob:none", "--no-checkout", url, path], **kwargs).check_returncode()

def fetch(base: str="git", **kwargs):
    subprocess.run([base, "fetch"], **kwargs).check_returncode()

def checkout(path: str, base: str="git", **kwargs):
    subprocess.run([base, "checkout", "origin/main", "--", path], **kwargs).check_returncode()

def add(path: str, base: str="git", **kwargs):
    subprocess.run([base, "add", path], **kwargs).check_returncode()

def commit(message: str, base: str="git", **kwargs):
    subprocess.run([base, "commit", "-m", message], **kwargs).check_returncode()

def push(base: str="git", **kwargs):
    subprocess.run([base, "push", "origin", "main"], **kwargs).check_returncode()

def remove(path: str, base: str="git", **kwargs):
    subprocess.run([base, "rm", path], **kwargs).check_returncode()