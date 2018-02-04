import os
import shutil
import yaml
import utils

YAML_EXT = '.yml'
COM_ROOT_PATH = os.path.join('/var/smartbox/com')

WEBUI_PATH = os.path.join(COM_ROOT_PATH, 'webui/')
IMAGES_PATH = os.path.join(WEBUI_PATH, 'images/')
SERVICE_CONFIGS_PATH = os.path.join(WEBUI_PATH, 'service_configs/')

FLIGHTCONTROL_PATH = os.path.join(COM_ROOT_PATH, 'flightcontrol/')
SERVICE_STATUSES_PATH = os.path.join(FLIGHTCONTROL_PATH, 'service_statuses/')
GLOBAL_STATUS_PATH = os.path.join(FLIGHTCONTROL_PATH, 'global_status' + YAML_EXT)
GLOBAL_CONFIGS_PATH = os.path.join(FLIGHTCONTROL_PATH,
                                   'global_config' + YAML_EXT)

HOST_PATH = os.path.join(COM_ROOT_PATH, 'host/')
VOLUMES_PATH = os.path.join(FLIGHTCONTROL_PATH, 'volumes/')
UUIDS_PATH = os.path.join(FLIGHTCONTROL_PATH, 'uuids/')
IMAGEIDS_PATH = os.path.join(FLIGHTCONTROL_PATH, 'imageids/')

#region file path helper


def get_service_config_path(service_name):
    return os.path.join(SERVICE_CONFIGS_PATH, service_name + YAML_EXT)


def get_service_status_path(service_name):
    return os.path.join(SERVICE_STATUSES_PATH, service_name + YAML_EXT)


def get_service_uuid_path(service_name):
    return os.path.join(UUIDS_PATH, service_name)


def get_service_image_path(service_name):
    return os.path.join(IMAGEIDS_PATH, service_name)


#region basic io


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


#region read


def read_global_config():
    global_config = _load_yaml_file(GLOBAL_CONFIGS_PATH)<
    validation_errors = validation.validate_global_config(global_config)
    if not validation_errors:
        return global_config
    else:
        print('global config validation error', global_config,
              validation_errors)


def read_global_status():
    global_status = _load_yaml_file(GLOBAL_STATUS_PATH)
    validation_errors = validation.validate_global_status(global_status)
    if not validation_errors:
        return global_status
    else:
        print('global status validation error', global_status, validation_errors)


def read_service_config(service_name):
    service_config = _load_yaml_file(get_service_config_path(service_name))
    validation_errors = validation.validate_service_status(service_config)
    if not validation_errors:
        return service_config
    else:
        print('service config validation error', service_name, service_config,
              validation_errors)


def read_service_names():
    return list(
        map(lambda fn: os.path.splitext(fn)[0],
            os.listdir(SERVICE_CONFIGS_PATH)))


def read_all_service_configs():
    service_configs = {}
    for service_name in read_service_names():
        service_configs[service_name] = read_service_config(service_name)
    return service_configs


def read_service_status(service_name):
    service_status = _load_yaml_file(get_service_status_path(service_name))
    validation_errors = validation.validate_service_status(service_status)
    if not validation_errors:
        return service_status
    else:
        print('service status validation error', service_name, service_status,
              validation_errors)


def read_all_service_statuses():
    service_statuses = {}
    for service_name in read_service_names():
        service_statuses[service_name] = read_service_status(service_name)
    return service_statuses


def read_service_uuid(service_name):
    """Returns the pod uuid for a service, if available"""
    uuid_path = get_service_uuid_path(service_name)
    if not os.path.exists(uuid_path):
        return None
    with open(uuid_path, 'r') as uuid_file:
        return uuid_file.readline()[:-1]  # remove \n at the end


def read_service_image_id(service_name):
    """Returns the image id for a service, if available"""
    image_id_path = get_service_image_path(service_name)
    if not os.path.exists(image_id_path):
        print('no imageID file', image_id_path)
        return None
    with open(image_id_path, 'r') as image_id_file:
        image_id_file_content = image_id_file.readline()
        image_id = image_id_file_content[:-1]  # remove \n at the end
        return image_id


#region write


def write_global_config(global_config):
    validation_errors = validation.validate_global_config(global_config)
    if not validation_errors:
        _dump_yaml_file(GLOBAL_CONFIGS_PATH, global_config)
    else:
        raise ValueError('global config validation error'
                         )  #, global_config, validation_errors


def write_global_status(global_status):
    validation_errors = validation.validate_global_status(global_status)
    if not validation_errors:
        _dump_yaml_file(GLOBAL_STATUS_PATH, global_status)
    else:
        raise ValueError('global status validation error'
                         )  #, global_status, validation_errors


def write_service_config(service_name, service_config):
    validation_errors = validation.validate_service_config(service_config)
    if not validation_errors:
        _dump_yaml_file(get_service_config_path(service_name), service_config)
    else:
        raise ValueError('service config validation error'
                         )  #, service_name, service_config, validation_errors


def write_service_status(service_name, service_status):
    validation_errors = validation.validate_service_status(service_status)
    if not validation_errors:
        _dump_yaml_file(get_service_status_path(service_name), service_status)
    else:
        raise ValueError('service status validation error'
                         )  #, service_name, service_status, validation_errors


def ensure_com_directories():
    """Creates all given directories, if not existing"""
    paths = [IMAGES_PATH, UUIDS_PATH, VOLUMES_PATH, IMAGEIDS_PATH]
    for dir_to_create in paths:
        globals.ensure_directory(dir_to_create)


#region convenience

#region misc
