import os
import unittest
from pathlib import Path

from sqlalchemy import inspect

from src.password.pwd_dto import PasswordNewEntry, SourceEntry, PasswordAddValuesDTO, PasswordValuesDTO
from src.password.pwd_repository import PasswordRepository, SecretsRepository


class PWDRepositoryTest(unittest.TestCase):
    """This tests the pwd repository, we should keep in mind that the input will be already sanitized"""
    def setUp(self):
        self.repository = PasswordRepository('test_table')
        self.repository.db.table('test_table_1')

    def test_save_valid(self):
        entry = PasswordNewEntry('test_username')
        self.assertEqual(len(self.repository.db.all()), 0)
        self.repository.save(entry)
        self.assertEqual(len(self.repository.db.all()), 1)

    def test_save_same_username(self):
        entry = PasswordNewEntry('test_username')
        self.assertEqual(len(self.repository.db.all()), 0)
        self.repository.save(entry)
        self.assertEqual(len(self.repository.db.all()), 1)
        self.repository.save(entry)
        self.assertEqual(len(self.repository.db.all()), 1)

    def test_save_invalid_object(self):
        entry = 'some_test'
        try:
            self.repository.save(entry)
        except Exception as ex:
            self.assertIsNotNone(ex)

    def test_get(self):
        entry_1 = PasswordNewEntry('user1')
        entry_1.sources = [
            SourceEntry(
                source_name = 'app1',
                source_pwd = '1234',
                previous_pwd = '444ttt',
                source_username='username_1'
            ),
            SourceEntry(
                source_name='app2',
                source_pwd='abc',
                previous_pwd='aabbcc',
                source_username='username_2'
            )
        ]
        self.repository.save(entry_1)

        entry_2 = PasswordNewEntry('user2')
        entry_2.sources = [
            SourceEntry(
                source_name = 'app55',
                source_pwd = 'fff',
                source_username='username_x'
            ),
            SourceEntry(
                source_name='app_new',
                source_pwd='ee',
                previous_pwd='44444',
                source_username='username_y'
            )
        ]
        self.repository.save(entry_2)

        # First lets test correctness of get function
        index, entry = self.repository.get('app1', 'user1')
        self.assertEqual(len(entry.sources), 1)
        self.assertEqual(index, 1)
        self.assertEqual(entry.sources[0], {'source_name': 'app1', 'source_pwd': '1234', 'previous_pwd':'444ttt', 'source_username':'username_1'})
        index, entry = self.repository.get('app2', 'user1')
        self.assertEqual(len(entry.sources), 1)
        self.assertEqual(index, 1)
        self.assertEqual(entry.sources[0], {'source_name': 'app2', 'source_pwd': 'abc', 'previous_pwd':'aabbcc', 'source_username':'username_2'})

        # Now let's get object that is not there
        index, entry = self.repository.get('app55', 'user1')
        self.assertEqual(index, 1)
        self.assertEqual(len(entry.sources), 0)

        # First lets test correctness of get function
        index, entry = self.repository.get('app_new', 'user2')
        self.assertEqual(len(entry.sources), 1)
        self.assertEqual(index, 2)
        self.assertEqual(entry.sources[0], {'source_name': 'app_new', 'source_pwd': 'ee', 'previous_pwd': '44444', 'source_username':'username_y'})

        # Now let's get object that is not there
        index, entry = self.repository.get('app1', 'user2')
        self.assertEqual(index, 2)
        self.assertEqual(len(entry.sources), 0)

        # Let's get object with user that is not there
        index, entry = self.repository.get('app1', 'user34')
        self.assertEqual(index, None)
        self.assertEqual(entry, None)

    def test_update(self):
        entry_1 = PasswordNewEntry('user1')
        entry_1.sources = [
            SourceEntry(
                source_name='app1',
                source_pwd='1234',
                source_username='username_1'
            ),
            SourceEntry(
                source_name='app2',
                source_pwd='abc',
                previous_pwd = '44433',
                source_username='username_2'
            )
        ]
        self.repository.save(entry_1)

        # update entry
        self.repository.update('app1', 'user1', 'new_password!')
        _, entry = self.repository.get('app1', 'user1')
        new_pwd = entry.sources[0]['source_pwd']
        old_pwd = entry.sources[0]['previous_pwd']
        self.assertEqual(new_pwd, 'new_password!')
        self.assertEqual(old_pwd, '1234')
        _, entry = self.repository.get('app2', 'user1')
        new_pwd = entry.sources[0]['source_pwd']
        old_pwd = entry.sources[0]['previous_pwd']
        self.assertEqual(new_pwd, 'abc')
        self.assertEqual(old_pwd, '44433')

        # remove an entry
        index, entry = self.repository.get('app2', 'user1')
        self.assertEqual(index, 1)
        self.assertEqual(len(entry.sources), 1)
        self.repository.update('app2', 'user1', '')
        index, entry = self.repository.get('app2', 'user1')
        self.assertEqual(index, 1)
        self.assertEqual(len(entry.sources), 0)

    def test_update_non_existent_entry_existing_user(self):
        entry_1 = PasswordNewEntry('user1')
        entry_1.sources = [
            SourceEntry(
                source_name='app1',
                source_pwd='1234',
                source_username='username_1'
            ),
            SourceEntry(
                source_name='app2',
                source_pwd='abc',
                previous_pwd = '44433',
                source_username='username_2'
            )
        ]
        self.repository.save(entry_1)

        # remove an entry that does not exist for user that exists -> adds new entry
        # {source_name = new_app2023!, source_pwd = password2023!}
        self.repository.update('new_app2023!', 'user1', 'password2023!')
        _, entry = self.repository.get('new_app2023!', 'user1')
        source_name = entry.sources[0]['source_name']
        new_pwd = entry.sources[0]['source_pwd']
        old_pwd = entry.sources[0]['previous_pwd']
        self.assertEqual(source_name, 'new_app2023!')
        self.assertEqual(new_pwd, 'password2023!')
        self.assertIsNone(old_pwd)
        # Let's update that to see that nothing breaks
        self.repository.update('new_app2023!', 'user1', 'new_password')
        _, entry = self.repository.get('new_app2023!', 'user1')
        new_pwd = entry.sources[0]['source_pwd']
        old_pwd = entry.sources[0]['previous_pwd']
        self.assertEqual(new_pwd, 'new_password')
        self.assertEqual(old_pwd, 'password2023!')

    def test_update_non_existing_entries(self):
        # update entry that does not exist for user that does not exist -> should do nothing
        self.repository.update('new_app2023!', 'user1', 'new_password')
        index, entry = self.repository.get('new_app2023!', 'user1')
        self.assertIsNone(index)
        self.assertIsNone(entry)

    def test_get_all_entries(self):
        entry_1 = PasswordNewEntry('user1')
        entry_1.sources = [
            SourceEntry(
                source_name='app1',
                source_pwd='1234',
                source_username='username_1'
            ),
            SourceEntry(
                source_name='app2',
                source_pwd='abc',
                previous_pwd='44433',
                source_username='username_2'
            )
        ]
        self.repository.save(entry_1)
        entries = self.repository.get_all('user1')
        self.assertListEqual([{'source_name': 'app1', 'source_pwd': '1234', 'previous_pwd': None, 'source_username':'username_1'}, {'source_name': 'app2', 'source_pwd': 'abc', 'previous_pwd': '44433', 'source_username':'username_2'}], entries)

    def tearDown(self):
        self.repository.db.drop_tables()
        self.repository.db.clear_cache()
        self.repository.db.close()
        os.remove(os.path.join(Path(os.getcwd()),'storage', 'test_table.json'))

class SecretRepositoryTest(unittest.TestCase):

    def setUp(self) -> None:
        self.repository = SecretsRepository('test_secrets')

    def tearDown(self):
        inspector = inspect(self.repository.engine)
        if self.repository.table in inspector.get_table_names():
            self.repository._drop_table()

    def test_3_users_were_saved(self):
        test_val_1 = PasswordAddValuesDTO('user1', 'secret', b'11233')
        test_val_2 = PasswordAddValuesDTO('user1', 'salt', b'334455')
        test_val_3 = PasswordAddValuesDTO('user2', 'secret', b'ddffrr')
        success = []
        for val in [test_val_1, test_val_2, test_val_3]:
            success.append(self.repository.save_value(val))
        self.assertEqual(success, [True, True, True])

    def test_save_empty_entry(self):
        test_val_1 = PasswordAddValuesDTO('', '', '')
        success = []
        for val in [test_val_1]:
            success.append(self.repository.save_value(val))
        self.assertEqual(success, [False])

    def test_save_existing_entry(self):
        test_val_1 = PasswordAddValuesDTO('user1', 'blook', b'11233')
        self.repository.save_value(test_val_1)
        test_val_1 = PasswordAddValuesDTO('user1', 'blook', b'11233')
        self.repository.save_value(test_val_1)

        value = self.repository.get_value(PasswordValuesDTO('user1', 'blook'))
        self.assertEqual(value.decode('utf-8'), '11233')

    def test_get_existing_value(self):
        entry_1 = PasswordAddValuesDTO('user1', 'bloop', b'11233')
        entry_2 = PasswordAddValuesDTO('user1', 'shwimp', b'334455')

        self.repository.save_value(entry_1)
        self.repository.save_value(entry_2)

        value = self.repository.get_value(PasswordValuesDTO('user1', 'bloop'))
        self.assertEqual(value.decode('utf-8'), '11233')

        new_value = self.repository.get_value(PasswordValuesDTO('user1', 'shwimp'))
        self.assertEqual(new_value.decode('utf-8'), '334455')

    def test_get_non_existing_value(self):
        value = self.repository.get_value(PasswordValuesDTO('user1087', 'sakura_234'))
        self.assertIsNone(value)

    def test_get_non_existing_value_for_user(self):
        entry_1 = PasswordAddValuesDTO('user1', 'rrrrr', '11233')
        entry_2 = PasswordAddValuesDTO('user1', 'ddsfdfsd', '334455')

        self.repository.save_value(entry_1)
        self.repository.save_value(entry_2)
        value = self.repository.get_value(PasswordValuesDTO('user1', 'serwerwerwersdjkfnskdfnsdf'))
        self.assertIsNone(value)


if __name__ == '__main__':
    unittest.main()
