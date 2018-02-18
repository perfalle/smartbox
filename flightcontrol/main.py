"""Flightcontrol runs in a privileged (fly) container.
It controls the container engine on the host via dbus and systemd.
The communication with the other internal containers in smartbox
is implemented as reading and writing files from and in
a common volume (cf. com module)."""

import time
import dbus
import apiservice
import systemd_services
import templates
import inotify.adapters
import sys
sys.path.append('..')
from common import com, utils

WEBUI_PORT = 8080


def restart_webui():
    """(Re)starts the webui service"""
    com.ensure_com_directories()
    content = templates.generate_webui_unit(WEBUI_PORT)
    systemd_services.restart(systemd_services.NAMESPACE_INTERNAL, "webui",
                             content)


def restart_apiservice():
    """(Re)starts the rkt api-service"""
    content = templates.generate_apiservice_unit()
    systemd_services.restart(systemd_services.NAMESPACE_INTERNAL, "apiservice",
                             content)


def remove_service(service_name):
    """Stops the service and removes all files associated with it (including volumes)"""
    stop_service(service_name)
    systemd_services.remove(systemd_services.NAMESPACE_RUN, service_name)
    systemd_services.remove(systemd_services.NAMESPACE_FETCH, service_name)
    com.rm_uuid_file(service_name)
    com.rm_image_id_file(service_name)
    com.rm_volumes(service_name)
    com.rm_reverse_proxy_site(service_name)


def fetch_service(service_name, service_config):
    """Begins to fetch the image for the service"""
    com.ensure_com_directories()
    content = templates.generate_fetching_unit(service_name, service_config)
    systemd_services.start(systemd_services.NAMESPACE_FETCH, service_name,
                           content)


def start_service(service_name, service_config):
    """Starts the service"""
    com.ensure_com_directories()
    content = templates.generate_running_unit(service_name, service_config)
    systemd_services.start(systemd_services.NAMESPACE_RUN, service_name,
                           content)


def restart_service(service_name, service_config):
    """Restarts the service"""
    com.ensure_com_directories()
    content = templates.generate_running_unit(service_name, service_config)
    systemd_services.restart(systemd_services.NAMESPACE_RUN, service_name,
                             content)


def stop_service(service_name):
    """Stops the service"""
    systemd_services.stop(systemd_services.NAMESPACE_FETCH, service_name)
    systemd_services.stop(systemd_services.NAMESPACE_RUN, service_name)
    com.rm_uuid_file(service_name)


def get_restart_required(service_name, service_config):
    """Checks if the service must be restarted due to changed configuration"""
    actual_content = systemd_services.get_content(
        systemd_services.NAMESPACE_RUN, service_name) or str()
    desired_content = templates.generate_running_unit(service_name,
                                                      service_config)
    # diff = utils.get_diff(actual_content, desired_content)
    # return 'ExecStart' in diff
    return actual_content != desired_content


def service_image_available(service_name):
    """Checks if the image of the service is available"""
    return apiservice.image_available(com.read_service_image_id(service_name))


def service_running(service_name):
    """Checks if the service is running"""
    return apiservice.running(com.read_service_uuid(service_name))


#def restore_backup(service_name, backup):
#def create_backup(service_name, backup):


def get_fetching_progress(service_name):
    """Returns the fetching progress of the service, if available and None otherwise"""
    utils.check_service_name(service_name)
    return 0


def get_settings_errors(service_name, service_config):
    """Checks service descriptons for configuration errors"""
    errors = []
    errors.append(utils.get_service_name_errors(service_name))
    return {}


def get_service_status(service_name, service_config):
    """Evaluates the status of a service"""
    status = {}
    img_available = service_image_available(service_name)
    running_desired = service_config.get('running', False)
    running = service_running(service_name)
    restart_required = get_restart_required(service_name, service_config)
    settings_errors = get_settings_errors(service_name, service_config)
    status['errors'] = settings_errors
    status['ports'] = apiservice.get_ports(
        com.read_service_image_id(service_name))
    status['mountpoints'] = apiservice.get_mountpoints(
        com.read_service_image_id(service_name))
    if img_available and running_desired and not settings_errors:
        if not running:
            status['state'] = 'starting'
        elif restart_required:
            status['state'] = 'restarting'
        else:
            status['state'] = 'running'
    elif not img_available and not running:
        if not settings_errors:
            status['state'] = 'fetching'
        else:
            status['state'] = 'noimage'
    elif running:
        status['state'] = 'stopping'
    else:
        status['state'] = 'stopped'
    return status


def update_services():
    """Updates all services to match the services.yml file"""
    service_configs = com.read_all_service_configs()
    loaded_services = systemd_services.get_loaded_services()
    services_to_remove = list(
        filter(lambda s: s not in service_configs, loaded_services))
    for service_name in services_to_remove:
        remove_service(service_name)
    statuses = {}
    for service_name in service_configs:
        service_config = service_configs[service_name] or {}
        service_status = get_service_status(service_name, service_config)
        com.write_service_status(service_name, service_status)
        statuses[service_name] = service_status
        print('evaluated status', service_name, service_status)
    # apply actions
    for service_name in statuses:
        service_state = statuses[service_name].get('state', None)
        service_config = service_configs[service_name]
        if service_state == 'fetching':
            fetch_service(service_name, service_config)
        elif service_state == 'starting':
            start_service(service_name, service_config)
        elif service_state == 'restarting':
            restart_service(service_name, service_config)
        elif service_state == 'stopping' or service_state == 'stopped':
            stop_service(service_name)


def on_com_changed(event):
    try:
        com.ensure_com_directories()
        update_services()
    except dbus.exceptions.DBusException as exception:
        # occurs sometimes at dbus calls TODO: do some investigations here
        print('dbus exception', exception)
    except Exception as exception:
        raise exception


def main():
    print('flightcontrol main')
    """Main method of smartbox flightcontrol"""
    # create com directories if not present
    com.ensure_com_directories()

    # start rkt api-service
    restart_apiservice()

    # check initial status of all installed services
    update_services()

    # prepare starting webui
    utils.ensure_directory(com.WEBUI_PATH)

    # ensure that internal services are started
    restart_webui()

    # listen to com events
    inotifyer = inotify.adapters.Inotify()
    inotifyer.add_watch(com.WEBUI_PATH)
    inotifyer.add_watch(com.SERVICE_CONFIGS_PATH)
    inotifyer.add_watch(com.IMAGEIDS_PATH)
    inotifyer.add_watch(com.UUIDS_PATH)
    try:
        for event in inotifyer.event_gen():
            if event is not None:
                (header, type_names, watch_path, filename) = event
                if 'IN_CLOSE_WRITE' in type_names or 'IN_DELETE' in type_names:
                    print(filename, type_names)
                    if filename:
                        print((header, type_names, watch_path, filename))
                        on_com_changed(None)
    finally:
        inotifyer.remove_watch(com.WEBUI_PATH)
        inotifyer.add_watch(com.SERVICE_CONFIGS_PATH)
        inotifyer.add_watch(com.IMAGEIDS_PATH)
        inotifyer.add_watch(com.UUIDS_PATH)


if __name__ == "__main__":
    main()
