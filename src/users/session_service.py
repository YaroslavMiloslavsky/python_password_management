import time

from src.interface.auth import AuthServiceInterface
from src.password.pwd_logic_service import PasswordLogicService
from src.password.pwd_repository import SecretsRepository
from src.users.user_dto import UserSaveDTO
from src.users.user_repository import UserRepository
from src.users.user_service import UserService
from src.utils.hashing_utils import HashingUtils
from src.utils.value_generation_util import ValueGenerator


class SessionService(AuthServiceInterface):
    def __init__(self, secret_table, user_table):
        super().__init__()
        self.password_service = PasswordLogicService(SecretsRepository(secret_table))
        self.users_service = UserService(UserRepository(user_table))

    def auth_user(self):
        user = self.users_service.get_user(self.username)
        if user is not None:
            user_username = user.username
            user_password = user.master_password
            secret = self.password_service.get_key(self.username)
            salt = self.password_service.get_salt(self.username)
            if self.username == user_username and self.password == HashingUtils.un_hash_value(user_password, secret, salt):
                print(f'Welcome back {self.username}')
                self.auth = True
                time.sleep(1)
            else:
                print('Wrong username or password, try again...')
                time.sleep(1)
        else:
            print('No username was found')
            time.sleep(1)

    def register_new_user(self):
        secret_key = ValueGenerator.generate_secret()
        salt = ValueGenerator.generate_salt()
        # Encrypt the password
        hashed_pwd = HashingUtils.hash_value(
            value= self.password,
            secret=secret_key,
            salt=salt
        )
        new_user = UserSaveDTO(
            username = self.username,
            password = hashed_pwd.decode()
        )
        user_saved = self.users_service.save_new_user(new_user)
        if user_saved:
            self.password_service.save_key(self.username, secret_key)
            self.password_service.save_salt(self.username, salt)
            self.auth = True
        else:
            print('Could not save user')
            time.sleep(1.5)

    def set_current_user(self, username, password):
        self.username = username
        self.password = password