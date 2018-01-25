import os
import shutil
import yaml
import utils

YAML_EXT = '.yml'
COM_ROOT_PATH = os.path.join('/var/smartbox/com')

WEBUI_PATH = os.path.join(COM_ROOT_PATH, 'webui/')
IMAGES_PATH = os.path.join(WEBUI_PATH, 'images/')
SERVICE_CONFIGS_PATH = os.path.join(WEBUI_PATH, 'service_configs/')
GLOBAL_CONFIGS_PATH = os.path.join(
    FLIGHTCONTROL_PATH, 'global_config' + YAML_EXT)

FLIGHTCONTROL_PATH = os.path.join(COM_ROOT_PATH, 'flightcontrol/')
SERVICE_STATES_PATH = os.path.join(FLIGHTCONTROL_PATH, 'service_states/')
GLOBAL_STATE_PATH = os.path.join(FLIGHTCONTROL_PATH, 'global_state' + YAML_EXT)

HOST_PATH = os.path.join(COM_ROOT_PATH, 'host/')
VOLUMES_PATH = os.path.join(FLIGHTCONTROL_PATH, 'volumes/')
UUIDS_PATH = os.path.join(FLIGHTCONTROL_PATH, 'uuids/')
IMAGEIDS_PATH = os.path.join(FLIGHTCONTROL_PATH, 'imageids/')


# file path helper

def get_service_config_path(service_name):
    return os.path.join(SERVICE_CONFIGS_PATH, service_name + YAML_EXT)


def get_service_state_path(service_name):
    return os.path.join(SERVICE_STATES_PATH, service_name + YAML_EXT)


def get_service_uuid_path(service_name):
    return os.path.join(UUIDS_PATH, service_name)


def get_service_image_path(service_name):
    return os.path.join(IMAGEIDS_PATH, service_name)


# read


def read_global_config():
    global_config = _load_yaml_file(GLOBAL_CONFIGS_PATH)
    validation_errors = validation.validate_global_config(global_config)
    if not validation_errors:
        return global_config
    else:
        print('global config validation error',
              global_config, validation_errors)


def read_global_state():
    global_state = _load_yaml_file(GLOBAL_STATE_PATH)
    validation_errors = validation.validate_global_state(global_state)
    if not validation_errors:
        return global_state
    else:
        print('global state validation error',
              global_state, validation_errors)


def read_service_config(service_name):
    service_config = _load_yaml_file(get_service_config_path(service_name))
    validation_errors = validation.validate_service_state(service_config)
    if not validation_errors:
        return service_config
    else:
        print('service config validation error',
              service_name, service_config, validation_errors)


def read_service_state(service_name):
    service_state = _load_yaml_file(get_service_state_path(service_name))
    validation_errors = validation.validate_service_state(service_state)
    if not validation_errors:
        return service_state
    else:
        print('service state validation error',
              service_name, service_state, validation_errors)


def read_service_uuid(service_name):
    """Returns the pod uuid for a service, if available"""
    uuid_path = get_service_uuid_path(service_name)
    if not os.path.exists(uuid_path):
        return None
    with open(uuid_path, 'r') as uuid_file:
        return uuid_file.readline()[:-1] # remove \n at the end


def read_service_image_id(service_name):
    """Returns the image id for a service, if available"""
    image_id_path = get_service_image_path(service_name)
    if not os.path.exists(image_id_path):
        print('no imageID file', image_id_path)
        return None
    with open(image_id_path, 'r') as image_id_file:
        image_id_file_content = image_id_file.readline()
        image_id = image_id_file_content[:-1] # remove \n at the end
        return image_id


# write

def write_global_config(global_config):
    validation_errors = validation.validate_global_config(global_config)
    if not validation_errors:
        _dump_yaml_file(GLOBAL_CONFIGS_PATH, global_config)
    else:
        raise ValueError('global config validation error'), global_config, validation_errors


def write_global_state(global_state):
    validation_errors = validation.validate_global_state(global_state)
    if not validation_errors:
        _dump_yaml_file(GLOBAL_STATE_PATH, global_state)
    else:
        raise ValueError('global state validation error'), global_state, validation_errors


def write_service_config(service_name, service_config):
    validation_errors = validation.validate_service_config(service_config)
    if not validation_errors:
        _dump_yaml_file(get_service_config_path(service_name), service_config)
    else:
        raise ValueError('service config validation error'), service_name, service_config, validation_errors


def write_service_state(service_name, service_state):
    validation_errors = validation.validate_service_state(service_state)
    if not validation_errors:
        _dump_yaml_file(get_service_state_path(service_name), service_state)
    else:
        raise ValueError('service state validation error'), service_name, service_state, validation_errors


# basic io

def _load_yaml_file(path):
    if not os.path.exists(path):
        return {}
    with open(path, 'r') as yaml_file:
        loaded_object = yaml.safe_load(yaml_file.read())
    return loaded_object or {}


def _dump_yaml_file(path, obj):
    utils.ensure_directory_of_file(path)
    with open(path, 'w+') as dump_file:
        dump_file.write(yaml.safe_dump(obj))
