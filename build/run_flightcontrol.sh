#!/bin/bash

mkdir -p /home/smartbox/com
rkt run --insecure-options=image \
 --stage1-name=coreos.com/rkt/stage1-fly:1.4.0 \
 --net=none \
 --volume unitfiles,kind=host,source="/etc/systemd/system" \
 --volume com,kind=host,source="/home/smartbox/com" \
 --volume dbussocketlocation,kind=host,source="/var/run/dbus" \
 --volume root,kind=host,source="/home/smartbox/flightcontrol" \
 flightcontrol.aci