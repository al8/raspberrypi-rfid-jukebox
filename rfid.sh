#!/bin/bash
#echo pid file $1
((/home/pi/raspberrypi-rfid-jukebox/rfid.py 2>&1) & echo $! >&3) 3> $1 | multilog /var/log/pyjuke-rfid &
