import unittest

from src.utils.value_generation_util import ValueGenerator


class PasswordGeneratorTest(unittest.TestCase):

    def test_pwd_generator_default(self):
        password = ValueGenerator.generate_password()
        self.assertIsNotNone(password)
        self.assertEqual(len(password), 10)
        self.assertNotIn(password, ',')

    def test_pwd_generator_too_short(self):
        password = ValueGenerator.generate_password(2)
        self.assertIsNotNone(password)
        self.assertEqual(len(password), 10)
        self.assertNotIn(password, ',')

    def test_pwd_generator_too_long(self):
        password = ValueGenerator.generate_password(255)
        self.assertIsNotNone(password)
        self.assertEqual(len(password), 32)
        self.assertNotIn(password, ',')


class SecretKeyGeneratorTest(unittest.TestCase):
    def test_secret_key_generator(self):
        secret = ValueGenerator.generate_secret()
        self.assertIsNotNone(secret)
        self.assertEqual(len(secret), 44)

class SecretSaltGeneratorTest(unittest.TestCase):
    def test_secret_salt_generator(self):
        salt = ValueGenerator.generate_salt()
        self.assertIsNotNone(salt)
        self.assertEqual(len(salt), 16)

if __name__ == '__main__':
    unittest.main()
