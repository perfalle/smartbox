"""Talks to rkt's api-service that must be running on the host"""

import json
import grpc
import api_pb2
import api_pb2_grpc

def image_available(image_id):
    """Checks if there is an image with the given id in rkt's local store"""
    if get_image_manifest(image_id):
        return True
    return False

def get_ports(image_id):
    """Returns the port mapping defined in the image manifest
    as dictionary: port_name -> internal port number"""
    manifest = get_image_manifest(image_id) or {}
    app = manifest.get('app', {}) or {}
    ports = {}
    for port_entry in app.get('ports', {}) or {}:
        name = port_entry.get('name', None)
        port = port_entry.get('port', None)
        if name and port:
            ports[name] = port
    return ports

def get_mountpoints(image_id):
    """Returns the mountpoint mapping defined in the image manifest
    as dictionary: mountpoint name -> mountpoint path"""
    manifest = get_image_manifest(image_id)
    app = manifest.get('app', {}) or {}
    mountpoints = {}
    for mountpoint_entry in app.get('mountPoints', {}) or {}:
        name = mountpoint_entry.get('name', None)
        path = mountpoint_entry.get('path', None)
        if name and path:
            mountpoints[name] = path
    return mountpoints

def running(uuid):
    """Checks if there is a pod running with the given uuid"""
    pod_state = _get_pod_state(uuid)
    if not pod_state:
        return False
    print('pod_state', pod_state)
    return pod_state == api_pb2.POD_STATE_RUNNING

def get_ip(uuid):
    """Returns the local ip of the pod in the default network
    Returns None, if there is no such pod or it is not running"""
    if not isinstance(uuid, str):
        return None
    try:
        inspect_pod_response = _get_inspect_pod_response(uuid)
        for network in inspect_pod_response.pod.networks:
            return network.ipv4
    except grpc._channel._Rendezvous as exception:
        return _handle_error(exception)
    return None

def get_isolators(uuid):
    """Returns the isolators of the pod"""
    raise NotImplementedError() #TODO: implement


def get_pod_manifest(uuid):
    """Returns the pod manifest of a given uuid, if available"""
    print('get_pod_manifest', uuid)
    if not isinstance(uuid, str):
        return None
    try:
        inspect_pod_response = _get_inspect_pod_response(uuid)
        manifest = json.loads(str(inspect_pod_response.manifest))
        if not manifest:
            manifest = {}
        return manifest
    except grpc._channel._Rendezvous as exception:
        return _handle_error(exception)

def get_image_manifest(image_id):
    """Returns the image manifest of a given image, if available"""
    if not isinstance(image_id, str):
        return {}
    try:
        inspect_image_request = api_pb2.InspectImageRequest()
        inspect_image_request.id = image_id
        inspect_image_response = _get_stub().InspectImage(inspect_image_request)
        manifest = json.loads(inspect_image_response.image.manifest.decode())
        return manifest or {}
    except grpc._channel._Rendezvous as exception:
        return _handle_error(exception) or {}

def _get_pod_state(uuid):
    """Returns the pod state of a given uuid, if available"""
    if not isinstance(uuid, str):
        return None
    try:
        return _get_inspect_pod_response(uuid).pod.state
    except grpc._channel._Rendezvous as exception:
        return _handle_error(exception)

def _get_inspect_pod_response(uuid):
    inspect_pod_request = api_pb2.InspectPodRequest()
    inspect_pod_request.id = uuid
    inspect_pod_response = _get_stub().InspectPod(inspect_pod_request)
    return inspect_pod_response

def _get_stub():
    channel = grpc.insecure_channel('localhost:15441')
    stub = api_pb2_grpc.PublicAPIStub(channel)
    return stub

def _handle_error(grpc_rendezvous_exception):
    print('_handle_error', grpc_rendezvous_exception)
    return None
    # details = grpc_rendezvous_exception.details()
    # print(details)
    # if details == 'Connect Failed':
    #     print('api-service not started/available!')
    #     raise grpc_rendezvous_exception
    # if details == 'unable to resolve UUID':
    #     return None
    # if 'ACI info not found with blob key' in details:
    #     return None
    # print('unknown error', details)
    # raise grpc_rendezvous_exception
