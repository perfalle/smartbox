#!/bin/bash

set -e
vagrant plugin install vagrant-scp

vagrant up --provider virtualbox
vagrant provision

mkdir -p ../install/images

# get flightcontrol
#vagrant ssh -c "sudo sha256sum /root/flightcontrol.aci"
vagrant scp smartboxbuild:/root/flightcontrol.aci ../install/images/flightcontrol.aci
#sha256sum smartbox/flightcontrol.aci

# get webui
#vagrant ssh -c "sudo sha256sum /root/webui.aci"
vagrant scp smartboxbuild:/root/webui.aci ../install/images/webui.aci
#sha256sum smartbox/webui.aci
