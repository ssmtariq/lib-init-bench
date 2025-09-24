import time
start_time = time.perf_counter()

# Inefficient: Using pkg_resources instead of importlib.metadata
import pkg_resources

# Calculate import time
import_time = time.perf_counter() - start_time

def get_package_version(package_name: str) -> str:
    """
    Get the version of an installed package using pkg_resources.
    This is inefficient as it builds a complete working set of packages.
    """
    try:
        return pkg_resources.get_distribution(package_name).version
    except pkg_resources.DistributionNotFound:
        return "not found"

def get_package_metadata(package_name: str) -> dict:
    """Get extended metadata for a package."""
    try:
        dist = pkg_resources.get_distribution(package_name)
        return {
            "name": dist.project_name,
            "version": dist.version,
            "location": dist.location,
            "requires": [str(r) for r in dist.requires()]
        }
    except pkg_resources.DistributionNotFound:
        return {
            "name": package_name,
            "error": "Package not found"
        }

def lambda_handler(event, context):
    """Return version information for a requested package."""
    package_name = event.get('package')
    
    if not package_name:
        return {
            'error': 'No package name provided',
            'import_time': import_time
        }
    
    # For simple version lookup, we could have used:
    # from importlib.metadata import version
    # version(package_name)
    # Instead of the heavy pkg_resources approach
    
    result = get_package_metadata(package_name)
    result['import_time'] = import_time
    
    return result