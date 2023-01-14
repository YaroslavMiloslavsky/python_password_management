import logging
import os
from typing import Final
from pathlib import Path

import sqlalchemy as db
from tinydb import TinyDB
from src.utils.logging_utils import Logger

PATH_TO_STORAGE: Final[str] = os.path.join(Path(os.getcwd()),'storage')
PATH_TO_SQL_DB: Final[str] = f'{PATH_TO_STORAGE}/logistics.sqlite'

class RepositoryInterface:
    """General interface, similar to interface keyword in Java"""
    def __init__(self, table_name):
        self._set_table(table_name)
        logger = Logger('user_repository', 'repository-logs', logging.NOTSET)
        self.logging = logger.get_logging()

    def _set_table(self, table_name: str):
        self.table = table_name

    def _initiate_db_connection(self):
        """Override this to init a connection to a Table"""
        pass

    def _drop_table(self):
        """Drops the table"""
        pass

class RepositorySQLInterface(RepositoryInterface):
    def __init__(self, table_name):
        super().__init__(table_name)
        self.engine = db.create_engine(f'sqlite:///{PATH_TO_SQL_DB}')
        self.metadata = db.MetaData()

class RepositoryNoSQLInterface(RepositoryInterface):
    def __init__(self, table_name):
        super().__init__(table_name)
        self.db = TinyDB(f'{PATH_TO_STORAGE}/{table_name}.json')

    def save(self, object_to_save):
        """Save the object -> Ensure to use : ObjectSaveDTO"""
        pass

    def get(self, object_name, username):
        """Depends on the implementation this should seek the object by this name"""
        pass

    def update(self, object_name, username, new_password):
        """Depends on the implementation this should update the object by this name"""
        pass

class UserSQLRepositoryInterface(RepositorySQLInterface):
    def __init__(self, table_name):
        super().__init__(table_name)

    def create_user(self, user):
        """Creates user in the system"""
        pass

    def find_user_by_username(self, username):
        """Finds user by username"""
        pass

    def delete_user_by_username(self, username):
        """Deletes user by username"""
        pass

class PasswordsRepositoryInterface(RepositoryNoSQLInterface):
    def __init__(self, table_name):
        super().__init__(table_name)

    def get_all(self, username):
        """Retrieves all the passwords"""
        pass

class PasswordGenerationVariablesRepositoryInterface(RepositorySQLInterface):
    def __init__(self, table_name):
        super().__init__(table_name)

    def save_value(self, entry):
        """Saves value into the DB"""
        pass

    def get_value(self, entry):
        """Retrieves the value from DB"""
        pass
