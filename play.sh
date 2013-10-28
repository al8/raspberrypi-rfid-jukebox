#!/bin/bash
# echo pid file $1
mkdir /tmp/monitor
((/home/pi/play/play.py 2>&1) & echo $! >&3) 3> $1 | multilog /var/log/playlog &
