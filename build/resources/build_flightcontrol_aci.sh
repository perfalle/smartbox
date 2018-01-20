#!/bin/bash

set -e
./acbuild --debug begin docker://debian
./acbuild --debug set-name flightcontrol
./acbuild --debug run -- apt-get update
./acbuild --debug run -- apt-get upgrade --yes
./acbuild --debug run -- apt-get install --yes python3.4 python3-pip  python3-yaml  libyaml-dev
./acbuild --debug run -- pip3 install watchdog grpcio Jinja2
./acbuild --debug run -- mkdir -p /home/smartbox/com
./acbuild --debug mount add com /home/smartbox/com
./acbuild --debug run -- mkdir -p /dbus
./acbuild --debug mount add dbussocketlocation /dbus
./acbuild --debug run -- mkdir -p /unitfiles
./acbuild --debug mount add unitfiles /unitfiles
./acbuild --debug mount add root /root
./acbuild --debug copy "./flightcontrol_startup.sh" "/startup.sh"
./acbuild --debug run -- chmod +x /startup.sh
./acbuild --debug set-exec -- /startup.sh
./acbuild --debug write --overwrite flightcontrol.aci
./acbuild --debug end
