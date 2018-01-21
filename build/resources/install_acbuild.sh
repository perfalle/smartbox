#!/bin/bash

set -e
if [[ -f ~/acbuild ]] ; then
    exit
fi
cd ~
git clone https://github.com/containers/build acbuild_repo
cd acbuild_repo
./build
 mv ./bin/acbuild ~/acbuild