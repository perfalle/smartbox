"""This module contains all communication with the webui via the common com volume."""

import os
import shutil
import yaml
import utils

COM_ROOT_PATH = '$SMARTBOX_HOME/com' # cf. os.path.expandvars(path)

WEBUI_PATH = os.path.join(COM_ROOT_PATH, 'webui')
IMAGES_PATH = os.path.join(WEBUI_PATH, 'images')
SERVICES_PATH = os.path.join(WEBUI_PATH, 'services.yml')

FLIGHTCONTROL_PATH = os.path.join(COM_ROOT_PATH, 'flightcontrol')
STATUS_PATH = os.path.join(FLIGHTCONTROL_PATH, 'status.yml')
ERRORS_PATH = os.path.join(FLIGHTCONTROL_PATH, 'errors.yml')
VOLUMES_PATH = os.path.join(FLIGHTCONTROL_PATH, 'volumes')
UUIDS_PATH = os.path.join(FLIGHTCONTROL_PATH, 'uuids')
REVPROXY_CONF_PATH = os.path.join(FLIGHTCONTROL_PATH, 'revproxyconf')
REVPROXY_SITES_PATH = os.path.join(FLIGHTCONTROL_PATH, 'revproxysites')
IMAGEIDS_PATH = os.path.join(FLIGHTCONTROL_PATH, 'imageids')


def get_service_descriptions():
    """Returns the service descriptions as provided by webui"""
    if not os.path.exists(SERVICES_PATH):
        return {}
    with open(SERVICES_PATH, 'r') as sd_file:
        service_descriptions = yaml.safe_load(sd_file.read())
    return service_descriptions or {}

def get_image_id(service_name):
    """Returns the image id for a service, if available"""
    image_id_path = os.path.join(IMAGEIDS_PATH, service_name)
    if not os.path.exists(image_id_path):
        print('no imageID file', image_id_path)
        return None
    with open(image_id_path, 'r') as image_id_file:
        image_id_file_content = image_id_file.readline()
        image_id = image_id_file_content[:-1] # remove \n at the end
        return image_id

def get_uuid(service_name):
    """Returns the pod uuid for a service, if available"""
    uuid_path = os.path.join(UUIDS_PATH, service_name)
    if not os.path.exists(uuid_path):
        return None
    with open(uuid_path, 'r') as uuid_file:
        return uuid_file.readline()[:-1] # remove \n at the end

def set_status(status):
    """Writes the status to the status.yml file for the webui to read"""
    utils.ensure_directory_of_file(STATUS_PATH)
    with open(STATUS_PATH, 'w+') as status_file:
        status_file.write(yaml.safe_dump(status))


def rm_uuid_file(service_name):
    """Removes the uuid file of the service"""
    uuid_path = os.path.join(UUIDS_PATH, service_name)
    if os.path.exists(uuid_path):
        os.remove(uuid_path)

def rm_image_id_file(service_name):
    """Removes the image id file of the service"""
    image_id_path = os.path.join(IMAGEIDS_PATH, service_name)
    if os.path.exists(image_id_path):
        os.remove(image_id_path)

def rm_volumes(service_name):
    """Removes all volumes of the service"""
    volume_path = os.path.join(VOLUMES_PATH, service_name)
    if os.path.exists(volume_path):
        shutil.rmtree(volume_path)

def rm_reverse_proxy_site(service_name):
    """Removes the reverse proxy's site configuration of the service"""
    site_path = os.path.join(REVPROXY_SITES_PATH, service_name)
    if os.path.exists(site_path):
        os.remove(site_path)


def ensure_com_directories():
    """Creates all given directories, if not existing"""
    for dir_to_create in [IMAGES_PATH, UUIDS_PATH, VOLUMES_PATH,
                          REVPROXY_CONF_PATH, REVPROXY_SITES_PATH, IMAGEIDS_PATH]:
        utils.ensure_directory(dir_to_create)
