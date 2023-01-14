import logging

from src.interface.repository import UserSQLRepositoryInterface
from src.interface.service import UserComponentInterface
from src.users.user_dto import UserSaveDTO, UserGetDTO
from src.utils.input_utils import UserInputUtil


class UserService(UserComponentInterface):

    def __init__(self, repository: UserSQLRepositoryInterface):
        super().__init__(repository)

    def get_user(self, username: str) -> UserGetDTO | None:
        is_valid, reasons = UserInputUtil.validate_username(username)
        if not is_valid:
            self.logging.error(f'Error: username is not valid due to {reasons}')
            return None
        self.logging.info('About to access data layer')
        found_user = self.repository.find_user_by_username(username)
        if found_user is None:
           logging.debug(f'User {username} does not exist')

        return found_user

    def save_new_user(self, user: UserSaveDTO) -> bool | None:
        #Validate user DTO
        #First validate the username
        is_valid, reasons = UserInputUtil.validate_username(user.username)
        if not is_valid:
            self.logging.error(f'Error: username is not valid due to {reasons}')
            return None
        #Validate the password
        is_valid, reasons = UserInputUtil.validate_password(user.master_password)
        if not is_valid:
            self.logging.error(f'Error: password is not valid due to {reasons}')
            return None
        return self.repository.create_user(user)

    def delete_user(self, username):
        is_valid, reasons = UserInputUtil.validate_username(username)
        if not is_valid:
            self.logging.error(f'Error: username is not valid due to {reasons}')
            return None

        return self.repository.delete_user_by_username(username)

