import datetime
import unittest
from unittest import mock

from src.users.user_dto import UserSaveDTO, UserGetDTO
from src.users.user_repository import UserRepository
from src.users.user_service import UserService


class UserServiceTest(unittest.TestCase):

    def setUp(self):
        self.repository_mock = mock.create_autospec(UserRepository)
        self.user_service = UserService(self.repository_mock)

    def test_create_user(self):
        user = UserSaveDTO('test_subject','some_password')
        is_saved = self.user_service.save_new_user(user)
        self.repository_mock.create_user.assert_called_once_with(user)
        self.assertTrue(is_saved)

    def test_invalid_username_illegal_symbols(self):
        user = UserSaveDTO('test=subject', 'some_password')
        is_saved = self.user_service.save_new_user(user)
        self.repository_mock.create_user.assert_not_called()
        self.assertFalse(is_saved)

    def test_invalid_username_too_long(self):
        user = UserSaveDTO('test_ttttttttttttttttttttttttttttttttttttttttttttttttt', 'some_password')
        is_saved = self.user_service.save_new_user(user)
        self.repository_mock.create_user.assert_not_called()
        self.assertFalse(is_saved)

    def test_invalid_username_too_short(self):
        user = UserSaveDTO('rt', 'some_password')
        is_saved = self.user_service.save_new_user(user)
        self.repository_mock.create_user.assert_not_called()
        self.assertFalse(is_saved)

    def test_invalid_password_illegal_too_long(self):
        user = UserSaveDTO('test_subject', 'a' * 340)
        is_saved = self.user_service.save_new_user(user)
        self.repository_mock.create_user.assert_not_called()
        self.assertFalse(is_saved)

    def test_invalid_password_illegal_too_short(self):
        user = UserSaveDTO('test_subject', '43r')
        is_saved = self.user_service.save_new_user(user)
        self.repository_mock.create_user.assert_not_called()
        self.assertFalse(is_saved)

    def test_get_user(self):
        username = 'test_username'
        created_at = datetime.datetime.now()
        self.repository_mock.find_user_by_username.return_value = UserGetDTO(username, '2233', created_at)
        found_user = self.user_service.get_user(username)
        self.repository_mock.find_user_by_username.assert_called_once()
        self.assertIsNotNone(found_user)

    def test_get_user_not_found(self):
        username = 'test_username'
        self.repository_mock.find_user_by_username.return_value = None
        found_user = self.user_service.get_user(username)
        self.repository_mock.find_user_by_username.assert_called_once()
        self.assertIsNone(found_user)

    def test_get_user_invalid_symbol(self):
        username = 'test_use=rna#$^me'
        created_at = datetime.datetime.now()
        self.repository_mock.find_user_by_username.return_value = UserGetDTO(username, '2233', created_at)
        found_user = self.user_service.get_user(username)
        self.repository_mock.find_user_by_username.assert_not_called()
        self.assertIsNone(found_user)

    def test_get_user_too_long(self):
        username = 'reeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeerrrrrrrrrrrrrrrrrrrr'
        created_at = datetime.datetime.now()
        self.repository_mock.find_user_by_username.return_value = UserGetDTO(username, '2233', created_at)
        found_user = self.user_service.get_user(username)
        self.repository_mock.find_user_by_username.assert_not_called()
        self.assertIsNone(found_user)

    def test_get_user_too_short(self):
        username = 'wer'
        created_at = datetime.datetime.now()
        self.repository_mock.find_user_by_username.return_value = UserGetDTO(username, '2233', created_at)
        found_user = self.user_service.get_user(username)
        self.repository_mock.find_user_by_username.assert_not_called()
        self.assertIsNone(found_user)

    def test_delete_user_valid(self):
        username = 'test_username'
        self.repository_mock.delete_user_by_username.return_value = True
        is_deleted = self.user_service.delete_user(username)
        self.assertTrue(is_deleted)

    def test_delete_user_invalid(self):
        username = 'test_username'
        self.repository_mock.delete_user_by_username.return_value = False
        is_deleted = self.user_service.delete_user(username)
        self.assertFalse(is_deleted)

    def test_delete_user_invalid_too_long(self):
        username = 'test_ussersersersersersersersersrsername'
        self.repository_mock.delete_user_by_username.return_value = True
        is_deleted = self.user_service.delete_user(username)
        self.assertIsNone(is_deleted)

    def test_delete_user_invalid_too_short(self):
        username = 'rr'
        self.repository_mock.delete_user_by_username.return_value = True
        is_deleted = self.user_service.delete_user(username)
        self.assertIsNone(is_deleted)

    def test_delete_user_invalid_symbols(self):
        username = 'test_=&*^&'
        self.repository_mock.delete_user_by_username.return_value = True
        is_deleted = self.user_service.delete_user(username)
        self.assertIsNone(is_deleted)

if __name__ == '__main__':
    unittest.main()
