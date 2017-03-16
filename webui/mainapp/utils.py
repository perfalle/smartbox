"""Utility functions"""

import os
import difflib

def get_diff(str1, str2):
    """Returns git-diff-like diff between two strings"""
    expected = str1.splitlines(1)
    actual = str2.splitlines(1)
    diff = difflib.unified_diff(expected, actual, lineterm=-0, n=0)
    return ''.join(diff)

def ensure_directory(path):
    """Creates the given directory, if not existing"""
    os.makedirs(path, exist_ok=True)

def ensure_directory_of_file(file_path):
    """Creates the parent directory of a given file path, if not existing"""
    ensure_directory(os.path.dirname(file_path))

def check_service_name(service_name):
    """Raises an exception if service_name is not valid"""
    service_name_errors = get_service_name_errors(service_name)
    if service_name_errors:
        raise Exception('errors: %s' % str(service_name_errors))

def get_service_name_errors(service_name):
    """Checks if service_name is valid and returns errors if it is not.
    Returns None if service_name is valid"""
    errors = []
    legal_characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789\\'
    for index in range(len(service_name)):
        if not service_name[index] in legal_characters:
            errors.append('Illegal character in service name: %s at position %s'
                          % (service_name[index], index))
    return errors
