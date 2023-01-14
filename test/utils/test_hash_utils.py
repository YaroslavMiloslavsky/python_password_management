import unittest

from src.utils.hashing_utils import HashingUtils
from src.utils.value_generation_util import ValueGenerator


class HashUtilsTest(unittest.TestCase):

    def setUp(self):
        self.password = ValueGenerator.generate_password(15)
        self.secret = ValueGenerator.generate_secret()
        self.salt = ValueGenerator.generate_salt()

    def test_hash_value(self):
        token = HashingUtils.hash_value(
            value= self.password,
            secret= self.salt,
            salt= self.salt
        )
        self.assertIsNotNone(token)
        self.assertNotEqual(token, self.password)

    def test_un_hash_value(self):
        token = HashingUtils.hash_value(
            value=self.password,
            secret=self.salt,
            salt=self.salt
        )
        unhashed_token = HashingUtils.un_hash_value(
            value=token,
            secret=self.salt,
            salt=self.salt
        )
        self.assertIsNotNone(unhashed_token)
        self.assertEqual(unhashed_token, self.password)


if __name__ == '__main__':
    unittest.main()
