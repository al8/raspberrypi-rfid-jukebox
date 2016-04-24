#!/usr/bin/env python

import os
import serial
import sys
import string

def writefile(data, filename, tmp_ext=".tmp"):
    tmp = "%s%s" % (filename, tmp_ext)
    with file(tmp, "wb") as f:
        f.write(data)
    os.rename(tmp, filename)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        serial_device = "/dev/ttyUSB0"
        outputfilename = "/tmp/monitor/rfid"
    else:
        serial_device = sys.argv[1]
        outputfilename = sys.argv[1]
    print "opening serial '%s'" % serial_device
    serial = serial.Serial(serial_device, baudrate=9600)
    code = ''

    # make the directory if it doesn't exist
    outputpath = os.path.dirname(outputfilename)
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)

    while True:
        data = serial.read()
        if data == '\r':
            c = ''.join(s for s in code.strip() if s in string.printable)

            print >> sys.stderr, len(c), c
             
            writefile(c, outputfilename)
            code = ''
        else:
            code += data
