import unittest

from sqlalchemy import inspect

from src.users.user_dto import UserSaveDTO
from src.users.user_repository import UserRepository

class UserRepositoryTest(unittest.TestCase):
    """This should test just the CRUD behind the repository, supposed that the input sanitized"""

    def setUp(self):
        self.repository = UserRepository('test_table')
        test_user_1 = UserSaveDTO('test1', '112233')
        test_user_2 = UserSaveDTO('test2', '33ddeee')
        test_user_3 = UserSaveDTO('test3', '33RRtt!')
        for user in [test_user_1, test_user_2, test_user_3]:
            self.repository.create_user(user)

    def test_find_user_valid(self):
        correct_username = 'test1'
        user = self.repository.find_user_by_username(correct_username)
        self.assertIsNotNone(user)

    def test_find_user_not_found(self):
        correct_username = 'test11'
        user = self.repository.find_user_by_username(correct_username)
        self.assertIsNone(user)

    def test_find_user_empty(self):
        correct_username = ''
        user = self.repository.find_user_by_username(correct_username)
        self.assertIsNone(user)

    def test_find_user_none(self):
        correct_username = None
        user = self.repository.find_user_by_username(correct_username)
        self.assertIsNone(user)

    def test_create_user(self):
        new_user = UserSaveDTO('test_new', '333222')
        found_user = self.repository.find_user_by_username(new_user.username)
        self.assertIsNone(found_user)
        self.repository.create_user(new_user)
        found_user = self.repository.find_user_by_username(new_user.username)
        self.assertIsNotNone(found_user)

    def test_create_user_none(self):
        new_user = None
        exception = None
        try:
            self.repository.create_user(new_user.username)
        except Exception as ex:
            exception = ex

        self.assertIsNotNone(exception)

    def test_create_user_empty(self):
        new_user = ''
        exception = None
        try:
            self.repository.create_user(new_user.username)
        except Exception as ex:
            exception = ex

        self.assertIsNotNone(exception)

    def test_create_user_int(self):
        new_user = 43
        exception = None
        try:
            self.repository.create_user(new_user.username)
        except Exception as ex:
            exception = ex

        self.assertIsNotNone(exception)

    def test_delete_user(self):
        found_user = self.repository.find_user_by_username('test1')
        self.assertIsNotNone(found_user)
        self.repository.delete_user_by_username('test1')
        found_user = self.repository.find_user_by_username('test1')
        self.assertIsNone(found_user)

    def test_drop_table(self):
        self.repository._drop_table()
        inspector = inspect(self.repository.engine)
        self.assertTrue(self.repository.table not in inspector.get_table_names())

    def tearDown(self):
        inspector = inspect(self.repository.engine)
        if self.repository.table in inspector.get_table_names():
            self.repository._drop_table()

if __name__ == '__main__':
    unittest.main()
