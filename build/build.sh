#!/bin/bash

set -e
vagrant plugin install vagrant-scp

vagrant up --provider virtualbox
vagrant provision

mkdir -p ansible

# get flightcontrol
#vagrant ssh -c "sudo sha256sum /root/flightcontrol.aci"
vagrant scp smartboxbuild:/root/flightcontrol.aci ansible/flightcontrol.aci
#sha256sum smartbox/flightcontrol.aci

# get webui
#vagrant ssh -c "sudo sha256sum /root/webui.aci"
vagrant scp smartboxbuild:/root/webui.aci ansible/webui.aci
#sha256sum smartbox/webui.aci

# copy install resources
./update_install_resources.sh