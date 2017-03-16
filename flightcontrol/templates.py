"""This module provides a methods to generate the content of
unit files and reverse proxy configuration with jinja2 templates"""

import os
from jinja2 import Environment, FileSystemLoader
import com
import utils
import apiservice

def _get_template_environment():
    local_directory = os.path.dirname(os.path.abspath(__file__))
    templates_directory = os.path.join(local_directory, 'templates')
    return Environment(autoescape=False,
                       loader=FileSystemLoader(templates_directory),
                       trim_blocks=True)

def generate_fetching_unit(service_name, service_description):
    """Generates the content of a oneshot unit file, that fetches the image for a service.
    It writes the image id to an image id file."""
    image_source = _get_image_source(service_description)
    image_id_path = os.path.join(com.IMAGEIDS_PATH, str(service_name))
    template = _get_template_environment().get_template('fetching.service')
    context = {'service_name': service_name,
               'image_source': image_source,
               'image_id_path': image_id_path}
    return template.render(context)

def generate_running_unit(service_name, service_description):
    """Generates the content of a unit file, that runs a rkt pod for the service.
    It writes the pod uuid to an uuid file."""
    image_id_path = os.path.join(com.IMAGEIDS_PATH, str(service_name))
    uuid_path = os.path.join(com.UUIDS_PATH, str(service_name))
    ports = service_description.get('ports', {}) or {}
    volumes = _get_and_ensure_volumes(service_name)
    context = {'service_name': service_name,
               'ports': ports,
               'volumes': volumes,
               'image_id_path': image_id_path,
               'uuid_path': uuid_path}
    return _get_template_environment().get_template('running.service').render(context)

def generate_reverse_proxy_site(service_name, service_description):
    """Generates the content of an Nginx site configuration (aka. service block),
    including hostname recognition, reverse proxy, SSL termination"""
    raise NotImplementedError() #TODO: implement

def generate_reverse_proxy_conf():
    """Generates the general configuration for Nginx"""
    raise NotImplementedError() #TODO: implement

def _get_image_source(service_description):
    src_types = ['source_url', 'source_file']
    if not 'source' in service_description:
        raise KeyError('Service description must contain a source field')
    src_type = service_description['source']
    if src_type not in src_types:
        raise KeyError('Invalid source type %s. Must be one of %s' % (src_type, src_types))
    if src_type not in service_description:
        raise KeyError('Source type "%s" not flund in service description' % src_type)
    src = service_description[src_type]
    if src_type == 'source_file':
        src = os.path.join(com.IMAGES_PATH, src)
    return src

def _get_and_ensure_volumes(service_name):
    volumes = {}
    for mountpoint in apiservice.get_mountpoints(com.get_image_id(service_name)):
        volumes[mountpoint] = os.path.join(com.VOLUMES_PATH, str(service_name))
        utils.ensure_directory(volumes[mountpoint])
    return volumes
