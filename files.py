import os

def list(path):
    files = os.listdir(path)
    files = map(lambda f: os.path.join(path, f), files)
    return sorted(filter(os.path.isfile, files))

