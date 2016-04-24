raspberrypi-rfid-jukebox
========================

Description:

    Play mp3s based on the rfid tag scanned! This works in two parts.
        rfid.py: reads RFID tags and updates a file (/tmp/monitor/rfid).
        play.py: monitors the rfid tag file (/tmp/monitor/rfid) and plays music.

Bill of Materials:

    Raspberry PI
    RFID Reader ID-12LA (125 kHz), Purchased from sparkfun.com, https://www.sparkfun.com/products/11827

Setup components:
    Checkout repo:
        cd /home/pi
        git clone https://github.com/al8/raspberrypi-rfid-jukebox.git
        (sorry, the code is really stupid right now)

    Connect USB RFID reader to USB port

    Install packages:
        sudo apt-get update
        sudo apt-get install daemontools
        sudo apt-get install alsa-utils mpg123


Verifying components:
    verify device has been added
        ls /dev/ttyUSB0
    setup temp directory
        mkdir /tmp/monitor
    check RFID tag
        ./rfid.py
        # it will say "opening serial '/dev/ttyUSB0'"
    scan a card
        12 66006C12A8B0

Music:
    Copy mp3 files into /home/pi/mp3
        example:
        ls -l /home/pi/mp3
        -rwxr-xr-x 1 pi pi 2538541 Aug 24  2011 01 - Twinkle Twinkle Little Star.mp3
        -rwxr-xr-x 1 pi pi 2857881 Aug 24  2011 02 - The Muffin Man.mp3
        -rwxr-xr-x 1 pi pi 2189884 Aug 24  2011 03 - The Puppet Show.mp3
        ...

    Create mapping between RFID tag and music
        Create file /home/pi/mp3/list.rfid
        File format:
            lines that start with '#'' are ignored
            example file:
            ######################
            # rfid_tag this is music.mp3
            12391789 twinkle twinkle.mp3
            12873182 ba ba black sheep.mp3
            ######################

Automation setup:
    copy monitors into /etc/init.d
        sudo ln -s /home/pi/raspberrypi-rfid-jukebox/init.d/pyjuke-rfid.sh /etc/init.d/pyjuke-rfid.sh
        sudo ln -s /home/pi/raspberrypi-rfid-jukebox/init.d/pyjuke-play.sh /etc/init.d/pyjuke-play.sh
    manually start the processes
        sudo /etc/init.d/pyjuke-rfid.sh start
        sudo /etc/init.d/pyjuke-play.sh start

Optional Setup:

    use ramdrive to prolong life of the sd card, add the follow line to /etc/fstab

        tmpfs    /tmp    tmpfs    defaults,noatime,nosuid,size=100m    0 0

    (mount -a to mount everything in fstab)

Debugging:
    manually restart the processes
        sudo /etc/init.d/pyjuke-rfid.sh restart
        sudo /etc/init.d/pyjuke-play.sh restart
    Look at logs:
        sudo tail -f /var/log/pyjuke-play/current
        sudo tail -f /var/log/pyjuke-rfid/current
