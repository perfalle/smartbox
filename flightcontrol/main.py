"""Flightcontrol runs in a privileged (fly) container.
It controls the container engine on the host via dbus and systemd.
The communication with the other internal containers in smartbox
is implemented as reading and writing files from and in
a common volume (cf. com module)."""

import time
import dbus
import utils
import apiservice
import com
import systemd_services
import templates
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def remove_service(service_name):
    """Stops the service and removes all files associated with it (including volumes)"""
    stop_service(service_name)
    systemd_services.remove(systemd_services.NAMESPACE_RUN, service_name)
    systemd_services.remove(systemd_services.NAMESPACE_FETCH, service_name)
    com.rm_uuid_file(service_name)
    com.rm_image_id_file(service_name)
    com.rm_volumes(service_name)
    com.rm_reverse_proxy_site(service_name)

def fetch_service(service_name, service_description):
    """Begins to fetch the image for the service"""
    com.ensure_com_directories()
    content = templates.generate_fetching_unit(service_name, service_description)
    systemd_services.start(systemd_services.NAMESPACE_FETCH, service_name, content)

def start_service(service_name, service_description):
    """Starts the service"""
    com.ensure_com_directories()
    content = templates.generate_running_unit(service_name, service_description)
    systemd_services.start(systemd_services.NAMESPACE_RUN, service_name, content)

def restart_service(service_name, service_description):
    """Restarts the service"""
    com.ensure_com_directories()
    content = templates.generate_running_unit(service_name, service_description)
    systemd_services.restart(systemd_services.NAMESPACE_RUN, service_name, content)

def stop_service(service_name):
    """Stops the service"""
    systemd_services.stop(systemd_services.NAMESPACE_FETCH, service_name)
    systemd_services.stop(systemd_services.NAMESPACE_RUN, service_name)
    com.rm_uuid_file(service_name)

def get_restart_required(service_name, service_description):
    """Checks if the service must be restarted due to changed configuration"""
    actual_content = systemd_services.get_content(systemd_services.NAMESPACE_RUN,
                                                  service_name) or str()
    desired_content = templates.generate_running_unit(service_name, service_description)
    diff = utils.get_diff(actual_content, desired_content)
    return 'ExecStart' in diff

def service_image_available(service_name):
    """Checks if the image of the service is available"""
    return apiservice.image_available(com.get_image_id(service_name))

def service_running(service_name):
    """Checks if the service is running"""
    return apiservice.running(com.get_uuid(service_name))

#def restore_backup(service_name, backup):
#def create_backup(service_name, backup):

def get_fetching_progress(service_name):
    """Returns the fetching progress of the service, if available and None otherwise"""
    utils.check_service_name(service_name)
    return 0

def get_settings_errors(service_name, service_description):
    """Checks service descriptons for configuration errors"""
    errors = []
    errors.append(utils.get_service_name_errors(service_name))
    return {}




def get_service_status(service_name, service_description):
    """Evaluates the status of a service"""
    status = {}
    img_available = service_image_available(service_name)
    running_desired = service_description.get('running_desired', False)
    running = service_running(service_name)
    restart_required = get_restart_required(service_name, service_description)
    settings_errors = get_settings_errors(service_name, service_description)
    status['errors'] = settings_errors
    status['ports'] = apiservice.get_ports(com.get_image_id(service_name))
    status['mountpoints'] = apiservice.get_mountpoints(com.get_image_id(service_name))
    if img_available and running_desired and not settings_errors:
        if not running:
            status['state'] = 'starting'
        elif restart_required:
            status['state'] = 'restarting'
        else:
            status['state'] = 'started'
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
    service_descriptions = com.get_service_descriptions()
    loaded_services = systemd_services.get_loaded_services()
    services_to_remove = list(filter(lambda s: s not in service_descriptions,
                                     loaded_services))
    for service_name in services_to_remove:
        remove_service(service_name)
    status = {}
    for service_name in service_descriptions:
        service_description = service_descriptions[service_name] or {}
        status[service_name] = get_service_status(service_name, service_description)
        print('evaluated status', service_name, status[service_name])
    com.set_status(status)
    # apply actions
    for service_name in status:
        state = status[service_name].get('state', None)
        service_description = service_descriptions[service_name]
        if state == 'fetching':
            fetch_service(service_name, service_description)
        elif state == 'starting':
            start_service(service_name, service_description)
        elif state == 'restarting':
            restart_service(service_name, service_description)
        elif state == 'stopping' or state == 'stopped':
            stop_service(service_name)



class ComEventHandler(FileSystemEventHandler):
    """Event handler class to recieve file modified events from watchdog observer"""
    def on_modified(self, event):
        try:
            com.ensure_com_directories()
            print(event.event_type, event.src_path)
            update_services()
        except dbus.exceptions.DBusException as exception:
            # occurs sometimes at dbus calls TODO: do some investigations here
            print('dbus exception', exception)
        except Exception as exception:
            raise exception

def main():
    """Main method of smartbox flightcontrol"""
    com.ensure_com_directories()
    utils.ensure_directory(com.WEBUI_PATH)
    directory_observer = Observer()
    directory_observer.schedule(ComEventHandler(), path=com.WEBUI_PATH, recursive=True)
    directory_observer.start()

    #TODO: run update_services on systemd events, too

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        directory_observer.stop()
    directory_observer.join()


if __name__ == "__main__":
    main()