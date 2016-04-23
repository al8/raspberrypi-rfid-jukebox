raspberrypi-rfid-jukebox
========================

Description:

Play mp3s based on the rfid tag scanned!

Bill of Materials:

    Raspberry pi
    RFID Reader ID-12LA (125 kHz), Purchased from sparkfun.com, https://www.sparkfun.com/products/11827
    mp3

Setup components:
    Checkout repo:
        cd /home/pi
        git clone https://github.com/al8/raspberrypi-rfid-jukebox.git
        (sorry, the code is really stupid right now)

    Connect USB RFID reader to USB port

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

Setup:
    copy monitors into /etc/init.d
        sudo cp ~/raspberrypi-rfid-jukebox/init.d/* /etc/init.d

Optional Setup:

    use ramdrive to prolong life of the sd card, add the follow line to /etc/fstab

        tmpfs    /tmp    tmpfs    defaults,noatime,nosuid,size=100m    0 0

    (mount -a to mount everything in fstab)

