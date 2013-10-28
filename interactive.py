#!/usr/bin/python

from chinput import HandleCh
from proc import Proc
from monitor import Monitor
import sys
import files
import types
import os
import time

def setup(musicpath, commandpath):
    global track_idx, proc
    track_idx = 0
    listmusic(musicpath)
    proc = Proc()
    global global_monitor
    global_monitor = Monitor(commandpath)

def listmusic(musicpath):
    global musicfiles, rfid_idxfilename_map
    files_list = files.list(musicpath)
    rfidfiles = filter(lambda f: f.endswith("rfid"), files_list)

    tmp_rfid_filename_map = {}
    for rfidfile in rfidfiles:
        with open(rfidfile) as f:
            for l in f:
                s = l.strip().split(" ", 1)
                if len(s) != 2:
                    # print "invalid rfid line: %s" % l.strip()
                    continue
                tmp_rfid_filename_map[s[0]] = s[1]

    rfid_idxfilename_map = {}
    musicfiles = filter(lambda f: f.endswith(".mp3"), files_list)
    print "num tracks: %d (%s)" % (len(musicfiles), musicpath)
    for idx, fname in enumerate(musicfiles):
        rfid_list = []
        for rfid, rfid_filename in tmp_rfid_filename_map.items():
            if os.path.basename(fname) == rfid_filename:
                rfid_idxfilename_map[rfid] = (idx, fname)
                rfid_list.append(rfid)
        rfid_list_str = " (RFID:%s)" % (",".join(rfid_list)) if rfid_list else ""
        print "%3d: %s%s" % (idx, os.path.basename(fname), rfid_list_str)
    print "rfid_idxfilename_map:"
    for rfid, (idx, fn) in rfid_idxfilename_map.items():
        print "  %s %d %s" % (rfid, idx, os.path.basename(fn))

def playtrack(fname):
    rc = proc.check()
    proc.run(["mpg321", fname])

def handler_per_loop():
    updated_files = global_monitor.update()
    if updated_files:
        print time.ctime(time.time()), "files updated", updated_files

    contents_l = []
    for filename in updated_files:
        with open(filename) as f:
            contents = f.read().strip()
            print "filename: %s. contents: %s" % (filename, contents)
            contents_l.append(contents)

    if not contents_l:
        return

    for c in contents_l:
        if c in rfid_idxfilename_map:
            idx, filename = rfid_idxfilename_map[c]
            global track_idx
            track_idx = idx
            space()
            return
    print "cannot find matching event for", contents_l

if __name__ == "__main__":
    if len(sys.argv) > 2:
        musicpath = sys.argv[1]
        commandpath = sys.argv[2]
    else:
        musicpath = "/home/pi/mp3/150 Fun Songs For Kids"
        commandpath = "/home/pi/mp3/monitor"

    setup(musicpath, commandpath)

    def p():
        global track_idx
        track_idx -= 1
        space()
    def n():
        global track_idx
        track_idx += 1
        space()
    def s():
        print "stop"
        proc.stop()
    def l():
        listmusic(musicpath)
        print "list", musicfiles
    def v():
        print "verify proc status"
        proc.check()
    def q():
        print "quit"
        sys.exit(0)
    def space():
        global track_idx
        if len(musicfiles) == 0:
            print "no music files"
            return
        track_idx %= len(musicfiles)
        trackname = musicfiles[track_idx]
        print "play", trackname
        playtrack(trackname)
    def h():
        print "handlers"
        print "\n".join(map(str, handlers.items()))

    handlers = {ord(" "): space}
    for char, fn in locals().items():
        if len(char) == 1 and isinstance(fn, types.FunctionType):
            handlers[ord(char)] = fn
    handlech = HandleCh(handlers, handler_per_loop=handler_per_loop)
    handlech.run()
