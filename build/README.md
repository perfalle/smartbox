# How to build and run smartbox
* run __build.sh__
* This creates the __ansible__ directory, containing an ansible role to install smartbox
* In the ansible directory run __ansible-playbook -i "*SERVER_IP* ," -u *REMOTE_USER* --ask-pass --ask-become-pass smartboxinstall.yml__

For more details about the build and install process, please visit the github wiki pages.
