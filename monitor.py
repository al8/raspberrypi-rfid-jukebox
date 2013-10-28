import os

def _list(path):
    files = os.listdir(path)
    files = map(lambda f: os.path.join(path, f), files)
    return sorted(filter(os.path.isfile, files))

class Monitor(object):
    def __init__(self, path):
        self.path = path
        self.last_state = {}
        self.update()

    def update(self):
        """
        returns list of modified files
        """
        filename_modified_map = {}
        for f in _list(self.path):
            filename_modified_map[f] = os.path.getmtime(f)

        # which new files are newer than the old file?
        modified_files = []
        for filename, mtime in filename_modified_map.items():
            if filename.endswith(".tmp"):
                continue
            if filename.endswith("~"):
                continue
            if os.path.basename(filename).startswith("."):
                continue
            if mtime > self.last_state.get(filename, 0):
                modified_files.append(filename)
        self.last_state = filename_modified_map
        return modified_files

if __name__ == "__main__":
    import sys, time
    m = Monitor(sys.argv[1])
    while True:
        print time.ctime(time.time()), "files updated", m.update()
        time.sleep(1)
