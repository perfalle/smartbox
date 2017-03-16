#!/bin/bash

mkdir -p /var/run/dbus
ln -s /dbus/system_bus_socket /var/run/dbus/system_bus_socket
exec python3 /root/main.py