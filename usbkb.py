#! /usr/bin/python
import struct
import select
import parse_keys

def has_data(fd, timeout=0.1):
    a = select.select([fd], [], [], timeout)
    b = ([fd], [], [])
    return a == b


EVFMT = "llHHi"
EVsize = struct.calcsize(EVFMT)

EV_SYN = 0x00
EV_KEY = 0x01
EV_REL = 0x02
EV_ABS = 0x03
EV_MSC = 0x04
EV_SW = 0x05
EV_LED = 0x11
EV_SND = 0x12
EV_REP = 0x14
EV_FF = 0x15
EV_PWR = 0x16
EV_FF_STATUS = 0x17
EV_MAX = 0x1f

class Event(object):
    """This structure is the collection of data for the general event
    interface. You can create one to write to an event device. If you read from
    the event device using a subclass of the EventDevice object you will get one of these.
    """
    def __init__(self, time=0.0, evtype=0, code=0, value=0):
        self.time = time # timestamp of the event in Unix time.
        self.evtype = evtype # even type (one of EV_* constants)
        self.code = code     # a code related to the event type
        self.value = value   # custom data - meaning depends on type above

    def __str__(self):
        return "Event:\n   time: %f\n evtype: 0x%x\n   code: 0x%x\n  value: 0x%x\n" % \
                    (self.time, self.evtype, self.code, self.value)

    def encode(self):
        tv_sec, tv_usec = divmod(self.time, 1.0)
        return struct.pack(EVFMT, long(tv_sec), long(tv_usec*1000000.0), self.evtype, self.code, self.value)

    def decode(self, ev):
        tv_sec, tv_usec, self.evtype, self.code, self.value = struct.unpack(EVFMT, ev)
        self.time = float(tv_sec) + float(tv_usec)/1000000.0

    def set(self, evtype, code, value):
        self.time = time.time()
        self.evtype = int(evtype)
        self.code = int(code)
        self.value = int(value)


file=open("/dev/input/event0")
keymap={
'\x2c': 'z',
'\x2d': 'x',
'\x2e': 'c',
'\xc8': 'UP',
'\xd0': 'DOWN',
'\xcb': 'LEFT',
'\xcd': 'RIGHT',
'\x10': 'q',
'\x11': 'w',
'\x12': 'e',
'\x01': 'ESC',
'\x2a': 'LSHIFT',
'\x1c': 'ENTER',
}
ord_key_map = parse_keys.parse()
while True:
    #if not has_data(file):
    #    print "nodata"
    #    continue
    event=file.read(16)
    e = Event()
    e.decode(event)
    if e.evtype == EV_KEY:
        state = ("released", "pressed", "repeat")[e.value]
        print state, e.code, ord_key_map.get(e.code, "unknown")
    else:
        print "#t:%s type:0x%x code:%s val:%s" % (e.time, e.evtype, e.code, e.value)
        pass
    # print len(event), ord(event[12])
    # if event[28] == '\x01':
    #     state="pressed:"
    # elif event[28] == '\x00':
    #     state="released:"
    # else:
    #     continue
    if e.code in keymap:
        print keymap[e.code]
file.close()

