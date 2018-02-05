"""
This module communicates with the dbus to control systemd services.
Reference for dbus calls: https://www.freedesktop.org/wiki/Software/systemd/dbus/

This module manages all systemd services used by smartbox.
The naming convention for unit files is as follows:
smartbox.internal.{service_name}.service    for internal services (webui, flightcontrol, revproxy)
smartbox.fetch.{service_name}.service       for fetching processes and
smartbox.run.{service_name}.service         for the rkt run commands, that actually run the pod
"""

import os
import glob
import dbus
import utils

UNIT_FILES_PATH = '/unitfiles'
UNIT_FILE_PREFIX = 'smartbox'
NAMESPACE_FETCH = 'fetch'
NAMESPACE_RUN = 'run'
NAMESPACE_INTERNAL = 'internal'
UNIT_FILE_SUFFIX = 'service'



def start(namespace, service_name, content):
    """Creates and startes a unit file with given content"""
    print('starting', namespace, service_name)
    unit_name = _get_unit_name(namespace, service_name)
    _create(unit_name, content)
    _get_manager().StartUnit(unit_name, 'fail')

def stop(namespace, service_name):
    """Stops the unit file, if available"""
    unit_name = _get_unit_name(namespace, service_name)
    print('stopping', unit_name)
    _get_manager().StopUnit(unit_name, 'fail')

def restart(namespace, service_name, content):
    """Restarts the unit file, if available"""
    print('restarting', namespace, service_name)
    unit_name = _get_unit_name(namespace, service_name)
    _create(unit_name, content)
    _get_manager().RestartUnit(unit_name, 'fail')

def remove(namespace, service_name):
    """Stops and removes the unit file, if available"""
    print('removing', namespace, service_name)
    stop(namespace, service_name)
    unit_name = _get_unit_name(namespace, service_name)
    unit_file_path = os.path.join(UNIT_FILES_PATH, unit_name)
    if os.path.isfile(unit_file_path):
        os.remove(unit_file_path)

def get_content(namespace, service_name):
    """Returns the content of the 'fetching' unit file, if available"""
    unit_name = _get_unit_name(namespace, service_name)
    unit_file_path = os.path.join(UNIT_FILES_PATH, unit_name)
    if os.path.isfile(unit_file_path):
        with open(unit_file_path, 'r') as unit_file:
            return unit_file.read()
    else:
        return str()

def get_property(namespace, service_name, property_name):
    """Returns the property of the specified unit"""
    unit_name = _get_unit_name(namespace, service_name)
    unit = _get_manager().LoadUnit(unit_name)
    unit_proxy = dbus.SystemBus().get_object('org.freedesktop.systemd1', str(unit))
    prop = unit_proxy.Get('org.freedesktop.systemd1.Unit', property_name,
                          dbus_interface='org.freedesktop.DBus.Properties')
    return prop

#def get_errors(namespace, service_name):
#    """Returns errors that occured while starting or running the unit file"""
#    return {}

#TODO: find a way to get fetch progress and log from any container to show in webui
#def get_logs(namespace, service_name):

def get_loaded_services(namespace=NAMESPACE_RUN):
    """Returns a list of services, that are loaded (as unit files) by the host system"""
    generic_unit_name = _get_unit_name(namespace, '*')
    generic_unit_path = os.path.join(UNIT_FILES_PATH, generic_unit_name)
    all_files = glob.glob(generic_unit_path)
    return list(map(lambda n:
                    n[len(UNIT_FILE_PREFIX) + len(namespace) + 2:-len(UNIT_FILE_SUFFIX) - 1],
                    map(os.path.basename, filter(os.path.isfile, all_files))))


def _create(unit_name, content):
    unit_file_path = os.path.join(UNIT_FILES_PATH, unit_name)
    #print('starting', unit_file_path)
    with open(unit_file_path, 'w+') as unit_file:
        unit_file.write(content)
    _reload_unit_files()

def _get_unit_name(namespace, service_name):
    valid_namespces = [NAMESPACE_FETCH, NAMESPACE_RUN, NAMESPACE_INTERNAL]
    if not namespace in valid_namespces:
        raise KeyError('invalid namespace "%s" must be one in %s' % (namespace, valid_namespces))
    # allow generic unit file name here
    if service_name != '*':
        utils.check_service_name(service_name)
    return '.'.join([UNIT_FILE_PREFIX, namespace, service_name, UNIT_FILE_SUFFIX])

def _reload_unit_files():
    _get_manager().Reload()

def _get_manager():
    systemd1 = dbus.SystemBus().get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
    return dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')
