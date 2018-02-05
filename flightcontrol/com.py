"""This module contains all communication with the webui via the common com volume."""

import os
import shutil
import yaml
import utils

from common.com import *


def get_service_configs():
    """Returns the service configs as provided by webui"""
    if not os.path.exists(SERVICES_PATH):
        return {}
    with open(SERVICES_PATH, 'r') as sd_file:
        service_configs = yaml.safe_load(sc_file.read())
    return service_configs or {}





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


