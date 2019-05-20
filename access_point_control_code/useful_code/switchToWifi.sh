#!/bin/bash

sudo sed  -i '/interface wlan0/s/^/#/' /etc/dhcpcd.conf
sudo sed  -i '/static ip_address=192.168.1.1*/s/^/#/' /etc/dhcpcd.conf
sudo sed  -i '/nohook wpa_supplicant/s/^/#/' /etc/dhcpcd.conf

sudo systemctl stop hostapd
sudo systemctl stop dnsmasq
sudo systemctl stop dhcpcd

tail -5 /etc/dhcpcd.conf


