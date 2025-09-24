import pytest
from handler import get_package_version, get_package_metadata, lambda_handler

def test_get_package_version():
    # Test with a package that's definitely installed (pip)
    version = get_package_version('pip')
    assert version != "not found"
    assert isinstance(version, str)

def test_get_package_version_nonexistent():
    version = get_package_version('nonexistent-package-xyz')
    assert version == "not found"

def test_get_package_metadata():
    # Test with pip which should be installed
    metadata = get_package_metadata('pip')
    assert metadata['name'] == 'pip'
    assert 'version' in metadata
    assert 'location' in metadata
    assert 'requires' in metadata

def test_get_package_metadata_nonexistent():
    metadata = get_package_metadata('nonexistent-package-xyz')
    assert metadata['name'] == 'nonexistent-package-xyz'
    assert 'error' in metadata

def test_lambda_handler():
    event = {'package': 'pip'}
    result = lambda_handler(event, None)
    assert result['name'] == 'pip'
    assert 'version' in result
    assert 'import_time' in result

def test_lambda_handler_no_package():
    event = {}
    result = lambda_handler(event, None)
    assert 'error' in result
    assert 'import_time' in result