#!/bin/bash

# in a line containing the given string, subsitute # with nothing 
sudo sed -i '/interface wlan0/s/^#//' /etc/dhcpcd.conf
sudo sed -i '/static ip_address=192.168.1.1/s/^#//' /etc/dhcpcd.conf
sudo sed -i '/nohook wpa_supplicant/s/^#//' /etc/dhcpcd.conf

# start access point programs
sudo systemctl start hostapd
sudo systemctl start dnsmasq
sudo systemctl start dhcpcd

# print last 5 lines to check that the comments have been removed
tail -5 /etc/dhcpcd.conf
