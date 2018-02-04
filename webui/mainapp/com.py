"""This module contains all communication with flightcontrol via the common com volume."""

import os
import yaml
from . import utils

COM_ROOT_PATH = '/var/smartbox/com'

WEBUI_PATH = os.path.join(COM_ROOT_PATH, 'webui')
IMAGES_PATH = os.path.join(WEBUI_PATH, 'images')
SERVICES_PATH = os.path.join(WEBUI_PATH, 'services.yml')

FLIGHTCONTROL_PATH = os.path.join(COM_ROOT_PATH, 'flightcontrol')
STATUS_PATH = os.path.join(FLIGHTCONTROL_PATH, 'status.yml')

def get_service_configs():
    """Returns the service configs"""
    return _load_yaml_file(SERVICES_PATH)

def get_status():
    """Returns the status of all services as provided by flightcontrol"""
    return _load_yaml_file(STATUS_PATH)

def set_running_desired(service_name, running_desired):
    """Updates running_desired in the services.yml file for flightcontrol"""
    _set_service_config_entry(service_name, 'running_desired', running_desired)

def set_ports(service_name, ports):
    """Updates ports entry in the services.yml file for flightcontrol"""
    _set_service_config_entry(service_name, 'ports', ports)

def add_service_config(service_name, service_config):
    """Adds a new service config to the services.yml file for flightcontrol"""
    service_configs = get_service_configs()
    service_configs[service_name] = service_config
    _set_service_configs(service_configs)

def remove_service_config(service_name):
    """Removes a service config from the services.yml file for flightcontrol"""
    service_configs = get_service_configs()
    if service_name in service_configs:
        service_configs.pop(service_name)
    _set_service_configs(service_configs)

def _set_service_configs(service_configs):
    _dump_yaml_file(SERVICES_PATH, service_configs)

def _set_service_config_entry(service_name, entry_name, entry_value):
    service_configs = get_service_configs()
    if service_name in service_configs:
        service_configs[service_name][entry_name] = entry_value
    _set_service_configs(service_configs)

def _load_yaml_file(path):
    if not os.path.exists(path):
        return {}
    with open(path, 'r') as yaml_file:
        loaded_object = yaml.safe_load(yaml_file.read())
    return loaded_object or {}

def _dump_yaml_file(path, obj):
    globals.ensure_directory_of_file(path)
    with open(path, 'w+') as dump_file:
        dump_file.write(yaml.safe_dump(obj))
