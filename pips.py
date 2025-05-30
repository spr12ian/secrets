pips = (
    "cachetools",  # For caching results
    "cryptography", # For encryption and decryption
    "google-auth", # For Google Drive authentication
    "google-auth-oauthlib", # For OAuth2 flow with Google Drive
    "google-api-python-client", # For Google Drive API client
    "PyYAML",  # For YAML file handling
    "setuptools",  # For packaging and installation
)


def get_pips():
    """
    Returns a tuple of pip packages required for the project.
    """
    return pips
