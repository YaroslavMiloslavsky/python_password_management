from src.interface.service import PasswordGeneratorLogicServiceInterface
from src.password.pwd_dto import PasswordValuesDTO, PasswordAddValuesDTO
from src.password.pwd_repository import SecretsRepository
from src.utils.input_utils import UserInputUtil
from src.utils.value_generation_util import ValueGenerator


class PasswordLogicService(PasswordGeneratorLogicServiceInterface):
    def __init__(self, pwd_storing_repository: SecretsRepository):
        super().__init__(pwd_storing_repository)

    def save_salt(self, username, salt):
        valid, reason = UserInputUtil.validate_username(username)
        if not valid:
            self.logging.error(f'Username is not valid due to {reason}')
            return None
        salt_entry = PasswordAddValuesDTO(username, 'salt', salt)
        self.pwd_storing_repository.save_value(salt_entry)

    def save_key(self, username, secret):
        valid, reason = UserInputUtil.validate_username(username)
        if not valid:
            self.logging.error(f'Username is not valid due to {reason}')
            return False
        key_entry = PasswordAddValuesDTO(username, 'secret', secret)
        self.pwd_storing_repository.save_value(key_entry)

    def get_salt(self, username):
        valid, reason = UserInputUtil.validate_username(username)
        if not valid:
            self.logging.error(f'Username is not valid due to {reason}')
            return None
        salt_entry = PasswordValuesDTO(username, 'salt')
        return self.pwd_storing_repository.get_value(salt_entry)

    def get_key(self, username):
        valid, reason = UserInputUtil.validate_username(username)
        if not valid:
            self.logging.error(f'Username is not valid due to {reason}')
            return None
        key_entry = PasswordValuesDTO(username, 'secret')
        return self.pwd_storing_repository.get_value(key_entry)

    def encrypt(self, password, key, salt):
        super().encrypt(password, key, salt)

    def decrypt(self, password, key, salt):
        super().decrypt(password, key, salt)

