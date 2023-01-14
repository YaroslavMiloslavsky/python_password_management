import unittest

from src.utils.input_utils import UserInputUtil

class InputUtilTest(unittest.TestCase):
    """Unit tests for input util"""
    def test_normal_username(self):
        username = 'testUser1'
        is_valid, reason = UserInputUtil.validate_username(username)
        self.assertEqual(True, is_valid)
        self.assertEqual(0, len(reason))

    def test_html_symbols(self):
        username = '<%^test%='
        is_valid, reason = UserInputUtil.validate_username(username)
        self.assertEqual(False, is_valid)
        self.assertGreater(len(reason), 1)

    def test_sql_injection(self):
        username = '=cmd(A | 0)'
        is_valid, reason = UserInputUtil.validate_username(username)
        self.assertEqual(False, is_valid)
        self.assertGreaterEqual(len(reason), 1)

    def test_username_too_long(self):
        username = 'werefsdfsdferwersdfefwerwersdfsdfsfewrwer'
        is_valid, reason = UserInputUtil.validate_username(username)
        self.assertEqual(False, is_valid)
        self.assertEqual(len(reason), 1)

    def test_username_too_short(self):
        username = 'erw'
        is_valid, reason = UserInputUtil.validate_username(username)
        self.assertEqual(False, is_valid)
        self.assertEqual(len(reason), 1)

    def test_normal_password(self):
        password = 'pwd1234'
        is_valid, reason = UserInputUtil.validate_password(password)
        self.assertEqual(True, is_valid)

    def test_password_too_long(self):
        password = 'tr' * 900
        is_valid, reason = UserInputUtil.validate_password(password)
        self.assertEqual(False, is_valid)
        self.assertEqual(len(reason), 1)

    def test_password_too_short(self):
        password = ''
        is_valid, reason = UserInputUtil.validate_password(password)
        self.assertEqual(False, is_valid)
        self.assertEqual(len(reason), 1)


if __name__ == '__main__':
    unittest.main()
