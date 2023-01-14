import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

class HashingUtils:
    @staticmethod
    def hash_value(value, secret, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=500000
        )
        key = base64.urlsafe_b64encode(kdf.derive(secret))
        encryption = Fernet(key)
        return encryption.encrypt(str.encode(value))

    @staticmethod
    def un_hash_value(value, secret, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=500000
        )
        key = base64.urlsafe_b64encode(kdf.derive(secret))
        encryption = Fernet(key)
        return encryption.decrypt(value).decode('utf-8')