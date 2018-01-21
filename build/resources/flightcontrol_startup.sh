#!/bin/bash
# This script is the entry point inside of the flightcontrol container.

set -e
mkdir -p /var/run/dbus
ln -s /dbus/system_bus_socket /var/run/dbus/system_bus_socket
exec python3 /etc/smartbox/flightcontrol/main.py