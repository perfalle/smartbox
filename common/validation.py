from jsonschema import Draft4Validator
import yaml, os

SCHEMAS_ROOT = os.path.join(os.path.dirname(__file__), 'schemas')
GLOBAL_CONFIG_SCHEMA_PATH = os.path.join(SCHEMAS_ROOT, 'global_config_schema.yml')
GLOBAL_STATUS_SCHEMA_PATH = os.path.join(SCHEMAS_ROOT, 'global_status_schema.yml')
SERVICE_CONFIG_SCHEMA_PATH = os.path.join(SCHEMAS_ROOT, 'service_config_schema.yml')
SERVICE_STATUS_SCHEMA_PATH = os.path.join(SCHEMAS_ROOT, 'service_status_schema.yml')


def validate_global_config(global_config):
    return _validate_with_schema(global_config, GLOBAL_CONFIG_SCHEMA_PATH)


def validate_global_status(global_status):
    return _validate_with_schema(global_config, GLOBAL_STATUS_SCHEMA_PATH)


def validate_service_config(service_config):
    return k_validate_with_schema(service_config, SERVICE_CONFIG_SCHEMA_PATH)


def validate_service_status(service_status):
    return _validate_with_schema(service_status, SERVICE_STATUS_SCHEMA_PATH)


def _validate_with_schema(obj, schema_file):
    with open(schema_file, 'r') as fd:
        validator = Draft4Validator(yaml.safe_load(fd.read()))
    return list(map(lambda ve: ve.message, validator.iter_errors(obj)))
