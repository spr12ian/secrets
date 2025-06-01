import os
import base64
import getpass
from typing import Optional
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend

SALT_SIZE = 16
ITERATIONS = 100_000


class EncryptionHelper:
    @staticmethod
    def derive_key(passphrase: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=ITERATIONS,
            backend=default_backend(),
        )
        return base64.urlsafe_b64encode(kdf.derive(passphrase.encode("utf-8")))

    @staticmethod
    def encrypt(data: bytes, passphrase: Optional[str] = None) -> bytes:
        if not passphrase:
            passphrase = getpass.getpass("Passphrase: ")
        salt = os.urandom(SALT_SIZE)
        key = EncryptionHelper.derive_key(passphrase, salt)
        fernet = Fernet(key)
        ciphertext = fernet.encrypt(data)
        return salt + ciphertext

    @staticmethod
    def decrypt(encrypted_data: bytes, passphrase: Optional[str] = None) -> bytes:
        if not passphrase:
            passphrase = getpass.getpass("Passphrase: ")
        salt = encrypted_data[:SALT_SIZE]
        ciphertext = encrypted_data[SALT_SIZE:]
        key = EncryptionHelper.derive_key(passphrase, salt)
        fernet = Fernet(key)
        return fernet.decrypt(ciphertext)
