# How to build and run smartbox

The following steps show how to run smartbox for development and testing.
DO NOT RUN smartbox this way for production!

## 1. Build the container images
The components of smartbox run in containers. To build the container images, set up a VM (e.g. Debian 8, 64 bit) with the following things installed:

 * acbuild (https://packages.debian.org/de/sid/acbuild)

Clone this repo into this VM and run __build\_flightcontrol\_aci.sh__ and __build\_webui\_aci.sh__ as root.
__flightcontrol.aci__ and __webui.aci__ will be created.
_NOTE:_ The container images are empty after build. They expect a volume for the python code when started.
_NOTE:_ Since the containers just contain all the dependencies and not the smartbox code itsself, you propably won't rebuild them too often.

For the next steps, you only need the generated files (__flightcontrol.aci__ and __webui.aci__).


## 2. Run smartbox
Requirements to run smartbox:

Linux OS with rkt and systemd (e.g. Debian 8, 64 bit).

Now the files from this repo need to be copied to the target system:
Create the directory __/opt/smartbox__ (or any other place) and set the environment variable __SMARTBOX\_HOME__ to that path.
Copy the __flightcontrol__ and __webui__ directories, as well as the __flightcontrol.aci__ and __webui.aci__ files to __SMARTBOX\_HOME__.
Finally copy __smartbox.service__ from the build directory to __/etc/systemd/system/__.


Now you can run smartbox with systemd: __systemctl start smartbox__