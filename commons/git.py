import subprocess

def clone(url: str, path: str, base: str="git", **kwargs):
    subprocess.run([base, "clone", url, path], **kwargs)

def fetch(base: str="git", **kwargs):
    subprocess.run([base, "fetch"], **kwargs)

def checkout(path: str, base: str="git", **kwargs):
    subprocess.run([base, "checkout", "origin/main", "--", path], **kwargs)

def add(path: str, base: str="git", **kwargs):
    subprocess.run([base, "add", path], **kwargs)

def commit(message: str, base: str="git", **kwargs):
    subprocess.run([base, "commit", "-m", f'"{message}"'], **kwargs)

def push(base: str="git", **kwargs):
    subprocess.run([base, "push", "origin", "main"], **kwargs)
