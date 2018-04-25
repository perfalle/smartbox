# How to build and run smartbox
* run __./build.sh__
* This creates the _install/images_ directory, containing the images for smartbox' internal containers.
* The _inatall_ directory contains an ansible role to install smartbox
* In the _inatall_ directory run __ansible-playbook -i "*SERVER_IP* ," -u *REMOTE_USER* --ask-pass --ask-become-pass smartboxinstall.yml__

For more details about the build and install process, please visit the github wiki pages.
