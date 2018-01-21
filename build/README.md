# How to build and run smartbox
* run __./build.sh__
* This creates the _ansible_ directory, containing an ansible role to install smartbox
* In the _ansible_ directory run __ansible-playbook -i "*SERVER_IP* ," -u *REMOTE_USER* --ask-pass --ask-become-pass smartboxinstall.yml__

For more details about the build and install process, please visit the github wiki pages.
