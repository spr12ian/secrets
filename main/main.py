from time import strftime
from cls_helper_google_drive import GoogleDriveHelper
from main.classes.yaml_helper import YamlHelper
import os
import sys
from pathlib import Path


# Configuration

VAULT_DIR = Path.home() / ".vault"
VAULT_FILE = Path(VAULT_DIR / "secrets.enc")
SALT_FILE = Path(VAULT_DIR / "vault.salt")
SETENV_FILE = Path(VAULT_DIR / "setenv.sh")
YAML_DECRYPTED_FILE = Path(VAULT_DIR / "dec.yaml")
YAML_ENV_FILE = Path(VAULT_DIR / "env.yaml")


def cloud_to_encrypted():
    # Download and decrypt a file from Google Drive
    drive_sync = GoogleDriveHelper()
    drive_sync.download_file("DRIVE_FILE_ID", VAULT_FILE)


def encrypted_to_cloud():
    timestamp = strftime("%Y-%m-%d_%H:%M:%S")
    source = Path(VAULT_FILE)
    target = f"{timestamp}_{source.name}"
    # Upload to Google Drive
    drive_sync = GoogleDriveHelper()
    drive_sync.upload_file(source, target)


def encrypted_to_yaml():
    vault_file = YamlHelper(VAULT_FILE)
    data = vault_file.read()

    decrypted_file = YamlHelper(YAML_DECRYPTED_FILE)
    decrypted_file.write(data)


def env_to_yaml():
    env_file = YamlHelper(YAML_ENV_FILE)
    env_file.write(dict(os.environ))


def yaml_to_encrypted():
    env_file = YamlHelper(YAML_ENV_FILE)
    data = env_file.read()

    vault_file = YamlHelper(VAULT_FILE)
    vault_file.write(data)


def yaml_to_env():
    """Load secrets from YAML file into environment variables."""
    env_file = YamlHelper(YAML_ENV_FILE)
    secrets = env_file.read()

    with open(SETENV_FILE, "w") as bash_file:
        bash_file.write(f"#!/bin/bash\n\n")
        for k, v in secrets.items():
            bash_file.write(f"export {k}={v}\n")
    print(
        f"Set {len(secrets)} environment variables by running `source {SETENV_FILE}`."
    )


if __name__ == "__main__":
    choices = {
        "env2yaml": env_to_yaml,
        "yaml2enc": yaml_to_encrypted,
        "enc2cloud": encrypted_to_cloud,
        "cloud2enc": cloud_to_encrypted,
        "enc2yaml": encrypted_to_yaml,
        "yaml2env": yaml_to_env,
    }
    keys = choices.keys()
    if len(sys.argv) != 2:
        print(f"Usage: pwl main.py {list(keys)}")
        print(len(sys.argv))
        sys.exit(1)

    choice = sys.argv[1]
    if choice not in choices:
        print(f"Invalid option. Use {', '.join(keys)}.")
        sys.exit(1)

    # Execute the chosen function
    choices[choice]()
