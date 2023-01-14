import secrets
import string
from typing import Final
import random

from cryptography.fernet import Fernet

DEFAULT_PWD_LENGTH :Final[int] = 10
MIN_PWD_LENGTH :Final[int] = 10
MAX_PWD_LENGTH :Final[int] = 32

class ValueGenerator:
    """Class for generating different values such as strings for passwords and secret keys"""

    @staticmethod
    def generate_password(password_length = DEFAULT_PWD_LENGTH):
        """Password length cannot be more than 32 and less than 10"""
        password_length = password_length if password_length > 10 else MIN_PWD_LENGTH
        password_length = password_length if password_length < 32 else MAX_PWD_LENGTH
        generated_password = []
        char_types = ['upper', 'lower', 'number', 'symbol']
        for _ in range(0, password_length):
            random.shuffle(char_types)
            char_type = random.choice(char_types)
            random_char = ''
            if char_type == 'upper':
                random_char = string.ascii_lowercase
            elif char_type == 'lower':
                random_char = string.ascii_lowercase
            elif char_type == 'number':
                random_char = string.digits
            else:
                random_char = string.punctuation

            generated_password.append(random.choice(random_char))
        return ''.join(generated_password)

    @staticmethod
    def generate_secret():
        return Fernet.generate_key()


    @staticmethod
    def generate_salt():
        return secrets.token_bytes(16)