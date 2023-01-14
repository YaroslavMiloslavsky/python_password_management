import logging

from src.users.user_dto import UserSaveDTO
from src.utils.logging_utils import Logger


class ServiceInterface:
    """General interface, similar to interface keyword in Java"""
    def __init__(self):
        logger = Logger('user_service', 'service-logs', logging.NOTSET)
        self.logging = logger.get_logging()

class UserComponentInterface(ServiceInterface):

    def __init__(self, repository):
        super().__init__()
        self.repository = repository

    def get_user(self, username: str):
        """Gets user from repository layer"""
        pass

    def save_new_user(self, user: UserSaveDTO):
        """Saves user to the repository layer"""
        pass

    def delete_user(self, username):
        """deletes user from the repository layer"""
        pass

class PasswordGeneratorLogicServiceInterface(ServiceInterface):
    """Interface for a service that stores manages the password main logic"""
    def __init__(self, pwd_storing_repository):
        """pwd_storing_repository is SQL repository that stores values for each user
            pwd_management_repository is NoSQL which stores the passwords"""
        super().__init__()
        self.pwd_storing_repository = pwd_storing_repository

    def save_salt(self, username, salt):
        """Generates and saves the salt"""
        pass

    def save_key(self, username, secret):
        """Generates and saves the key"""
        pass

    def get_salt(self, username):
        """Gets the salt"""
        pass

    def get_key(self, username):
        """Gets the key"""
        pass

    def encrypt(self, password, key, salt):
        """Encrypts the password"""
        pass

    def decrypt(self, password, key, salt):
        """Decrypts the password"""
        pass