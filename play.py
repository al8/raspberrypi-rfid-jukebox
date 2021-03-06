#!/usr/bin/env python

from chinput import HandleCh
from proc import Proc
from monitor import Monitor
import sys
import files
import types
import os
import time
import signal

def sig_handler(signum=None, frame=None):
    print 'Signal handler called with signal', signum
    sys.exit(0)

def setup(musicpath, commandpath):
    global g_track_idx, g_proc
    g_track_idx = 0
    listmusic(musicpath)
    g_proc = Proc()
    global global_monitor
    global_monitor = Monitor(commandpath)
    global g_last_fname
    g_last_fname = None
    global global_monitor_musicpath
    global_monitor_musicpath = Monitor(musicpath)

    for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
        signal.signal(sig, sig_handler)

def listmusic(musicpath):
    """
    look in musicpath for *.rfid files
        rfid files are in the format of:
        lines that start with '#'' are ignored
        example file:
        -----------
        # rfid_tag this is music.mp3
        12391789 twinkle twinkle.mp3
        12873182 ba ba black sheep.mp3
        -----------

    look in musicpath for *.mp3 files and store them in g_musicfiles
    """
    global g_musicfiles, g_rfid_idxfilename_map
    files_list = files.list(musicpath)
    rfidfiles = filter(lambda f: f.endswith(".rfid"), files_list)

    tmp_rfid_filename_map = {}
    for rfidfile in rfidfiles:
        with open(rfidfile) as f:
            for l in f:
                l = l.strip()
                if len(l) == 0:  # blank lines
                    continue
                if l[0] == "#":  # a comment
                    continue
                s = l.strip().split(" ", 1)
                if len(s) != 2:
                    # print "invalid rfid line: %s" % l.strip()
                    continue
                tmp_rfid_filename_map[s[0]] = s[1]

    g_rfid_idxfilename_map = {}
    g_musicfiles = filter(lambda f: f.endswith(".mp3"), files_list)
    print >> sys.stderr, "num tracks: %d (%s)" % (len(g_musicfiles), musicpath)
    for idx, fname in enumerate(g_musicfiles):
        rfid_list = []
        for rfid, rfid_filename in tmp_rfid_filename_map.items():
            rfid = rfid.strip().upper()
            if rfid_filename == os.path.basename(fname):
                g_rfid_idxfilename_map[rfid] = (idx, fname)
                rfid_list.append(rfid)
                break
        rfid_list_str = " (RFID:%s)" % (",".join(rfid_list)) if rfid_list else ""
        print >> sys.stderr, "%3d: %s%s" % (idx, os.path.basename(fname), rfid_list_str)
    print >> sys.stderr, "rfid_idxfilename_map:"
    for rfid, (idx, fn) in g_rfid_idxfilename_map.items():
        print >> sys.stderr, "  %s %d %s" % (rfid, idx, os.path.basename(fn))

def playtrack(fname):
    global g_last_fname
    rc = g_proc.check()
    if g_proc.is_running():
        if g_last_fname == fname:
            print >> sys.stderr, "same file already playing %s" % fname
            return
    g_proc.run(["/usr/bin/mpg123", fname])
    g_last_fname = fname

def playindex():
    global g_track_idx
    if len(g_musicfiles) == 0:
        print >> sys.stderr, "no music files"
        return
    g_track_idx %= len(g_musicfiles)
    trackname = g_musicfiles[g_track_idx]
    print >> sys.stderr, "play", trackname
    playtrack(trackname)

def stop():
    g_proc.stop()
    print >> sys.stderr, "stop"

def handler_per_loop():
    proc_rc = g_proc.check()

    global g_track_idx
    updated_files = global_monitor.update()
    if updated_files:
        print >> sys.stderr, time.ctime(time.time()), "files updated", updated_files

    contents_l = []
    for filename in updated_files:
        try:
            with open(filename) as f:
                contents = f.read().strip()
                print >> sys.stderr, "filename: %s. contents: %s" % (filename, contents)
                contents_l.append(contents)
        except IOError as ex:
            print >> sys.stderr, "unable to open file '%s' %s" % (filename, ex)

    if not contents_l:
        return

    for c in contents_l:
        c_rfid = c.strip().upper()
        if c_rfid in g_rfid_idxfilename_map:
            idx, filename = g_rfid_idxfilename_map[c_rfid]
            g_track_idx = idx
            playindex()
            print >> sys.stderr, "found rfid '%s' playing %d:'%s'" % (c_rfid, idx, os.path.basename(filename))
            continue
        elif c.startswith("play ") or c.startswith("p "):
            s = c.split();
            if len(s) > 2 and s[1] == "idx":
                try:
                    g_track_idx = int(s[2])
                except ValueError:
                    print >> sys.stderr, "invalid track index '%s'" % c
                    continue
                playindex()
            elif len(s) > 2 and s[1] == "substring":
                idx_fn_list = []
                for idx, m in enumerate(g_musicfiles):
                    if s[2].lower() in os.path.basename(m).lower():
                        idx_fn_list.append((idx, m))
                if len(idx_fn_list) > 0:
                    if (idx_fn_list) > 1:
                        print >> sys.stderr, "multiple files match, choosing first one"
                        for idx, m in idx_fn_list:
                            print >> sys.stderr, "   ", idx, m
                    idx, m = idx_fn_list[0]  # grab only first command
                    g_track_idx = idx
                    playindex()
                    print >> sys.stderr, "play track substring '%s' found at %d:'%s'" % (s[2], idx, os.path.basename(m))
                    continue
            else:
                print >> sys.stderr, "unknown play command '%s'" % (c)
                continue
        elif c == "stop" or c == "s":
            stop()
            continue
        else:
            print >> sys.stderr, "unknown command '%s'" % c
            continue
    # end for c

def handler_monitor_musicpath():
    updated_files = global_monitor_musicpath.update()
    if updated_files:
        listmusic(global_monitor_musicpath.path)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        musicpath = sys.argv[1]
        commandpath = sys.argv[2]
    else:
        musicpath = "/home/pi/mp3"
        commandpath = "/tmp/monitor"

    setup(musicpath, commandpath)

    # def p():
    #     global g_track_idx
    #     g_track_idx -= 1
    #     space()
    # def n():
    #     global g_track_idx
    #     g_track_idx += 1
    #     space()
    # def s():
    #     stop()
    # def l():
    #     listmusic(musicpath)
    #     print "list", g_musicfiles
    # def v():
    #     print "verify proc status"
    #     g_proc.check()
    # def q():
    #     print "quit"
    #     sys.exit(0)
    # def space():
    #     playindex()
    # def h():
    #     print "handlers"
    #     print "\n".join(map(str, handlers.items()))

    # handlers = {ord(" "): space}
    # for char, fn in locals().items():
    #     if len(char) == 1 and isinstance(fn, types.FunctionType):
    #         handlers[ord(char)] = fn
    # handlech = HandleCh(handlers, handler_per_loop=handler_per_loop)
    # handlech.run()

    while True:
        handler_per_loop()
        handler_monitor_musicpath()
        time.sleep(.1)
