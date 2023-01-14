import unittest
from unittest import mock

from src.password.pwd_dto import PasswordAddValuesDTO
from src.password.pwd_logic_service import PasswordLogicService
from src.password.pwd_repository import SecretsRepository


class PasswordLogicServiceTest(unittest.TestCase):

    def setUp(self) -> None:
        self.repository_mock = mock.create_autospec(SecretsRepository)
        self.pwd_logic_service = PasswordLogicService(self.repository_mock)

    def test_save_key_valid(self):
        self.pwd_logic_service.save_key('user1', 'any')
        new_value = PasswordAddValuesDTO(
            username='user1',
            key='secret',
            value='any'
        )
        self.repository_mock.save_value.assert_called_once()
        saved_value = self.repository_mock.save_value.call_args.args[0]
        self.assertEqual(new_value.username, saved_value.username)
        self.assertEqual(new_value.key, saved_value.key)
        self.assertIsNotNone(saved_value.value)
        self.assertGreaterEqual(len(saved_value.value), 1)

    def test_save_salt_valid(self):
        self.pwd_logic_service.save_salt('user1', 'any')
        new_value = PasswordAddValuesDTO(
            username='user1',
            key='salt',
            value='any'
        )
        self.repository_mock.save_value.assert_called_once()
        saved_value = self.repository_mock.save_value.call_args.args[0]
        self.assertEqual(new_value.username, saved_value.username)
        self.assertEqual(new_value.key, saved_value.key)
        self.assertIsNotNone(saved_value.value)
        self.assertGreaterEqual(len(saved_value.value), 1)

    def test_get_key_valid(self):
        self.pwd_logic_service.get_key('user1')
        self.repository_mock.get_value.assert_called_once()

    def test_get_salt_valid(self):
        self.pwd_logic_service.get_salt('user1')
        self.repository_mock.get_value.assert_called_once()



if __name__ == '__main__':
    unittest.main()