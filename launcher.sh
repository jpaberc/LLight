#!/bin/sh
# launcher.sh
# navigate to the home directory, then to this directory, then execute LLight, then back home

sleep 10
cd /home/pi/llight
sudo python llight.py
cd /
