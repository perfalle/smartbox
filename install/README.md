# How to build and run smartbox
First, go to the _build_ directory and follow the instructions in the _README.md_ there
* To install smartbox run __ansible-playbook -i "*SERVER_IP* ," -u *REMOTE_USER* --ask-pass --ask-become-pass smartboxinstall.yml__
* To run a VM with smartbox locally, run __vagrant up__ and __vagrant provision__.

## Note:
Vagrant up may fail with an gpg related error due to the "Install rkt (Debian/Ubuntu)"-Task of the ansible role.
However if you then run vagrant provision, it works fine.


For more details about the build and install process, please visit the github wiki pages.