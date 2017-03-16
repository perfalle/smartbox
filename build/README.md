##How to build and run smartbox

The following steps show how to run smartbox for development and testing.
DO NOT RUN smartbox this way for production!

#1. Build the containers
Requirements to run smartbox:

Linux OS with acbuild and all dependencies as needed by the _build\_\*\_aci.sh_-scripts
Run these scripts as root.

_NOTE:_ The containers are empty after build. They expect a volume for the python code when started.

#2. Run smartbox
Requirements to run smartbox:

Linux OS with rkt, acbuild and systemd.

Add a user _smartbox_ and add grant it all sudo privileges and add it to the rkt group.

Copy the following files to /home/smartbox:
* build/\*.aci
* build/run\_\*.sh
* flightcontrol/\*
* webui/\*

Remove all other files or directories.

Run the run\_\*.sh_-scripts as root.

_NOTE:_ It is not necessary to rebuild the containers unless the dependencies have changed. Just update the source files and restart the containers.