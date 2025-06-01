from main.classes.encryption_helper import EncryptionHelper
from pathlib import Path
from typing import Optional
import yaml


class YamlHelper:
    def __init__(self, file_path: Path):
        match file_path.suffix:
            case ".enc":
                self.encrypted = True
            case ".yaml":
                self.encrypted = False
            case _:
                raise ValueError(f"File {file_path} is not a [encrypted] YAML file.")
        self.file_path = file_path

    def read(self, passphrase: Optional[str] = None) -> dict:
        if not self.file_path.exists():
            raise FileNotFoundError(f"{self.file_path} not found.")

        if self.encrypted:
            encrypted_bytes = self.file_path.read_bytes()
            plaintext = EncryptionHelper.decrypt(encrypted_bytes, passphrase)
            return yaml.safe_load(plaintext) or {}
        else:
            return yaml.safe_load(self.file_path.read_text(encoding="utf-8")) or {}

    def write(self, data: dict, passphrase: Optional[str] = None):
        yaml_text = yaml.dump(data, default_flow_style=False).encode("utf-8")

        if self.encrypted:
            encrypted_bytes = EncryptionHelper.encrypt(yaml_text, passphrase)
            self.file_path.write_bytes(encrypted_bytes)
        else:
            self.file_path.write_text(yaml_text.decode("utf-8"), encoding="utf-8")

        print(f"Data written to {self.file_path}")
