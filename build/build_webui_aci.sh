#!/bin/bash

acbuild --debug begin docker://python
acbuild --debug set-name webui
acbuild --debug run -- pip3 install django
acbuild --debug run -- pip3 install pyyaml
acbuild --debug run -- mkdir -p home/smartbox/com
acbuild --debug mount add com home/smartbox/com
acbuild --debug mount add root root
acbuild --debug port add webuihttp tcp 80
acbuild --debug set-exec -- python /root/manage.py runserver 0.0.0.0:80
acbuild --debug write --overwrite webui.aci
acbuild --debug end