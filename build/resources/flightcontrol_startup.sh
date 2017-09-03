#!/bin/bash
# This script is the entry point inside of the flightcontrol container.

mkdir -p /var/run/dbus
ln -s /dbus/system_bus_socket /var/run/dbus/system_bus_socket
exec python3 /root/main.py