import sys
import select
import tty
import termios

# http://code.activestate.com/recipes/134892/
class Getch:
    def __init__(self, select_timeout=0.1):
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
        #tty.setraw(self.fd)
        tty.setcbreak(self.fd)
        self.select_timeout = select_timeout

    def _is_data(self, fd):
        a = select.select([fd], [], [], self.select_timeout)
        b = ([fd], [], [])
        return a == b

    def __call__(self):
        try:
            if not self._is_data(self.fd):
                return None
            ch = sys.stdin.read(1)
        except Exception as e:
            print e
            ch = None
        #finally:
        #    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def __del__(self):
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)


class HandleCh(object):
    def __init__(self, ord_handler_map, handler_per_loop=None):
        self.getch = Getch()
        self.ord_handler_map = ord_handler_map
        self.handler_per_loop = handler_per_loop

    def run(self, debug=False, exit_ord=3):
        while True:
            x = self.getch()
            if self.handler_per_loop:
                self.handler_per_loop()
            if x is None:
                continue
            if debug:
                print "ord(key)=%s handler=%s" % (ord(x), self.ord_handler_map.get(ord(x), None))
            if ord(x) in self.ord_handler_map:
                self.ord_handler_map[ord(x)]()
            if ord(x) == exit_ord:
                sys.exit(0)

if __name__ == "__main__":
    import time
    getch = Getch()
    while True:
        x = getch()
        if x is None:
            continue
        print "%s: %s" % (ord(x), x)
        if ord(x) == 3:
            sys.exit(0)
