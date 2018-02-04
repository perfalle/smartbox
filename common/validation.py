from jsonschema import Draft4Validator
import yaml

GLOBAL_CONFIG_SCHEMA_PATH = 'schemas/global_config_schema.yml'
GLOBAL_STATUS_SCHEMA_PATH = 'schemas/global_status_schema.yml'
SERVICE_CONFIG_SCHEMA_PATH = 'schemas/service_config_schema.yml'
SERVICE_STATUS_SCHEMA_PATH = 'schemas/service_status_schema.yml'


def validate_global_config(global_config):
    return _validate_with_schema(global_config, GLOBAL_CONFIG_SCHEMA_PATH)


def validate_global_status(global_status):
    return _validate_with_schema(global_config, GLOBAL_STATUS_SCHEMA_PATH)


def validate_service_config(service_config):
    return _validate_with_schema(global_config, SERVICE_CONFIG_SCHEMA_PATH)


def validate_service_status(service_status):
    return _validate_with_schema(global_config, SERVICE_STATUS_SCHEMA_PATH)


def _validate_with_schema(obj, schema_file):
    with open(schema_file, 'r') as fd:
        validator = Draft4Validator(fd.safe_load(yaml_file.read()))
    return list(map(lambda ve: ve.message, validator.iter_errors(obj)))
