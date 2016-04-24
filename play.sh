#!/bin/bash
# echo pid file $1
((/home/pi/raspberrypi-rfid-jukebox/play.py 2>&1) & echo $! >&3) 3> $1 | multilog /var/log/pyjuke-play &
