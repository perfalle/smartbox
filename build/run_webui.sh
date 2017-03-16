#!/bin/bash

mkdir -p /home/smartbox/com
rkt run --insecure-options=image \
 --net=default --port=webuihttp:8080 \
 --volume com,kind=host,source="/home/smartbox/com" \
 --volume root,kind=host,source="/home/smartbox/webui" \
 webui.aci \
