#!/bin/bash
#echo pid file $1
mkdir /tmp/monitor
((/home/pi/play/rfid.py 2>&1) & echo $! >&3) 3> $1 | multilog /var/log/rfidlog &
#echo $! > $1
#((/home/pi/play/rfid.py) & echo $! >&3) 3> $1 > /var/log/rfidlog &
