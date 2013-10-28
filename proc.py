import subprocess
import sys
import time

class Proc(object):
    """
    makes sure we're only running a single process in the background
    """
    def __init__(self, debug=False):
        self.current = None
        self.p = None
        self.debug = debug
        self.last_returncode = None

    def run(self, command):
        self._cleanup()
        self.p = subprocess.Popen(command, shell=False, stdout=sys.stdout, stderr=sys.stderr)

    def stop(self):
        self._cleanup()

    def check(self):
        if self.p is None:
            if self.debug:
                print "check: p is None"
            return self.last_returncode
        rc = self.p.poll()
        if self.debug:
            print "check: %s" % rc
        if rc is None:
            return None
        self.last_returncode = rc
        self.p = None
        return rc

    def is_running(self):
        self.check()
        return not (self.p is None)

    def _cleanup(self):
        if self.p is not None:
            self.p.terminate()
        self.p = None

    def __del__(self):
        self._cleanup()

if __name__ == "__main__":
    #p = subprocess.Popen(['sleep', '5'], shell=False, stdout=subprocess.PIPE)
    p = Proc(debug=True)
    p.run(["sleep", "5"])
    while True:
        rc = p.check()
        time.sleep(0.3)

