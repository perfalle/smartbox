import os
from datetime import datetime
import urllib.parse
from django.shortcuts import render, redirect
from .forms import AddForm, PortForm
import sys
sys.path.append('..')
from common import com, utils


def show(request):
    service_names = com.read_service_names()
    service_contexts = []
    for service_name in service_names:
        service_config = com.read_service_config(service_name)
        service_status = com.read_service_status(service_name)
        service_contexts.append(
            get_service_context(service_name, service_config, service_status))
    context = {'services': service_contexts}
    return render(request, 'show.html', context)


def start(request):
    service_name = str(request.path)[len('/start/'):]
    com.set_running(service_name, True)
    return redirect('/service/' + str(service_name))


def stop(request):
    service_name = str(request.path)[len('/stop/'):]
    com.set_running(service_name, False)
    #return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/show'))
    return redirect('/service/' + str(service_name))


def add(request):
    if request.method == 'POST':
        form = AddForm(request.POST, request.FILES)
        if form.is_valid():
            print('valid', request.POST, request.FILES)
            service_config = dict()
            if 'imagefile' in request.FILES:
                file = request.FILES['imagefile']
                handle_uploaded_file(file)
                service_config['source_file'] = file.name
            else:
                service_config['source_url'] = request.POST['url']

            service_config['ports'] = {}
            #service_config['volumes'] = {}
            #service_config['backup_strategies'] = None
            service_config['running'] = False
            com.write_service_config(request.POST['service_name'],
                                     service_config)
            return redirect('/show')
        else:
            print('not valid', request.POST, request.FILES)
    else:
        form = AddForm()
    return render(request, 'add.html', {'form': form})


def handle_uploaded_file(f):
    utils.ensure_directory(com.IMAGES_PATH)
    with open(os.path.join(com.IMAGES_PATH, f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def remove(request):
    service_name = str(request.path)[len('/remove/'):]
    com.rm_service_config(service_name)
    return redirect('/show')


def get_service_context(service_name, service_config, service_status):
    service_context = dict()
    service_context['service_name'] = service_name
    service_context['state'] = service_status.get('state',
                                                  'noimage') or 'noimage'
    service_context['url_service_name'] = urllib.parse.quote(
        service_name)  # -> urllib.parse.unquote
    service_context['active_status'] = service_status.get('ActiveState',
                                                          '-') or '-'
    service_context['sub_status'] = service_status.get('SubState', '-') or '-'
    utc_time = max(
        int(service_status.get('ActiveEnterTimestamp', 0) or 0),
        int(service_status.get('ActiveExitTimestamp', 0)) or 0)
    service_context['time'] = str(datetime.fromtimestamp(utc_time))
    if 'source_url' in service_config:
        service_context['source'] = service_config['source_url'] or str()
        service_context['source_type'] = 'url'
    elif 'source_file' in service_config:
        service_context['source'] = service_config['source_file'] or str()
        service_context['source_type'] = 'file'
    service_context['ports'] = service_status.get('ports', {}) or {}
    service_context['volumes'] = service_status.get('volumes', {}) or {}
    service_context['backups'] = service_config.get('backups', {}) or {}
    return service_context


def service(request):
    service_name = str(request.path)[len('/service/'):]
    service_status = com.read_service_status(service_name)
    service_config = com.read_service_config(service_name)

    service_context = get_service_context(service_name, service_config,
                                          service_status)
    context = dict()
    context['service'] = service_context

    old_ports = service_config.get('ports', {}) or {}
    print('old_ports', old_ports)
    for port_name in service_status.get('ports', {}) or {}:
        old_ports[port_name] = old_ports.get(port_name, None)
    port_form = PortForm(request.POST or None, request.FILES or None)
    port_form.add_ports(old_ports)
    if request.method == 'POST':
        if port_form.is_valid():
            new_ports = service_context['ports']
            for port_name in service_context['ports']:
                direct_field_name = port_form.get_direct_field_name(port_name)
                proxy_field_name = port_form.get_proxy_field_name(port_name)
                hostname_field_name = port_form.get_hostname_field_name(
                    port_name)
                try:
                    direct_port = int(request.POST[direct_field_name])
                except (TypeError, ValueError):
                    direct_port = None
                try:
                    proxy_port = int(request.POST[proxy_field_name])
                except (TypeError, ValueError):
                    proxy_port = None
                hostname = request.POST[hostname_field_name]
                new_ports[port_name] = {
                    'direct_port': direct_port,
                    'proxy_port': proxy_port,
                    'hostname': hostname
                }
            print(new_ports)
            #TODO: check for illegal port mappings
            com.set_ports(service_name, new_ports)
            return redirect('/service/' + str(service_name))
        else:
            print('not valid', request.POST, request.FILES)

    context['port_form'] = port_form
    print(service)
    print(context)
    return render(request, 'service.html', context)
