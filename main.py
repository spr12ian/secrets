import base64
from time import strftime
from cls_helper_encryption import EncryptionHelper
from cls_helper_google_drive import GoogleDriveHelper
from cls_helper_yaml import YamlHelper
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import sys
import getpass
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


def decrypt_encrypted() -> dict:
    passphrase = getpass.getpass("Passphrase: ")
    fernet = get_fernet(passphrase)
    try:
        plaintext = fernet.decrypt(VAULT_FILE.read_bytes())
        return yaml.safe_load(plaintext)
    except Exception as e:
        print("Decryption failed:", str(e))
        return {}


def derive_key(passphrase: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend(),
    )
    return base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))


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


def get_fernet(passphrase: str) -> Fernet:
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    if not SALT_FILE.exists():
        SALT_FILE.write_bytes(os.urandom(16))
    salt = SALT_FILE.read_bytes()
    key = derive_key(passphrase, salt)
    return Fernet(key)


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
    print(f"Set {len(secrets)} environment variables by running `source {SETENV_FILE}`.")


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
