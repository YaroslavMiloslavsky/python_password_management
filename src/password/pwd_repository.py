import datetime

import sqlalchemy as db
from sqlalchemy import Sequence, insert, select, update
from tinydb import Query

from src.interface.repository import PasswordsRepositoryInterface, PasswordGenerationVariablesRepositoryInterface
from src.password.pwd_dto import PasswordNewEntry, SourceEntry, PasswordGetEntry, PasswordAddValuesDTO, \
    PasswordValuesDTO


class PasswordRepository(PasswordsRepositoryInterface):

    def __init__(self, table_name):
        super().__init__(table_name)

    def save(self, object_to_save: PasswordNewEntry):
        """For saving new entry"""
        entry_id = None
        query = Query()
        if type(object_to_save) is PasswordNewEntry and \
                len(self.db.search(query.username == object_to_save.username)) == 0:
            self.logging.debug(f'New password is about to be saved for {object_to_save.username}')
            try:
                entry_id = self.db.insert(object_to_save.to_json())
            except Exception as ex:
                self.logging.error(f'Error during saving: {ex}')
        return entry_id

    def get(self, object_name: str, username: str) -> (int, PasswordGetEntry):
        documents = None
        entry_id = None
        self.logging.debug(f'Getting password for {object_name}')
        query = Query()
        try:
            documents = self.db.search(query.username == username)
            entry_id = documents[0].doc_id if len(documents) > 0 else None
        except Exception as ex:
            self.logging.error(f'Error: {ex}')
        sources = list(filter(lambda x: x['source_name'] == object_name, documents[0]['sources'])) if len(
            documents) > 0 and documents is not None else None
        return entry_id, PasswordGetEntry(username=username, sources=sources) if sources is not None else None

    def update(self, object_name: str, username: str, new_password: str, source_username: str = None):
        """For adding and removing passwords
            New password is empty? delete the entry"""
        self.logging.debug(f'Updating {object_name} for {username}')
        query = Query()
        changed_index = None
        try:
            sources = self.db.search(query.username == username)
            # If the password empty we remove the password
            if len(new_password) == 0 or new_password is None:
                updated_sources = [source for source in sources[0]['sources'] if source['source_name'] != object_name]
                changed_index = self.db.update({'sources': updated_sources}, query.username == username)
            else:
                updated, updated_sources = PasswordRepository.change_password(sources, object_name, new_password)
                if not updated:
                    new_entry = SourceEntry(
                        source_name=object_name,
                        source_pwd=new_password,
                        previous_pwd=None,
                        source_username=source_username
                    )
                    sources[0]['sources'].append(new_entry.to_json())
                changed_index = self.db.update({'sources': updated_sources}, query.username == username)
        except Exception as ex:
            self.logging.error(f'Error during update of {username}, {object_name}, {ex}')
        return changed_index[0] if changed_index is not None and len(changed_index) > 0 else []

    def get_all(self, username: str):
        self.logging.debug(f'Getting all entries for {username}')
        query = Query()
        entries = None
        try:
            entries = self.db.search(query.username==username)
        except Exception as ex:
            self.logging.error(f'Exception {ex} while getting all entries for {username}')
        return entries[0]['sources']

    @staticmethod
    def change_password(sources, object_name, new_password):
        updated = False
        for source in sources[0]['sources']:
            if source['source_name'] == object_name:
                source['previous_pwd'] = source['source_pwd']
                source['source_pwd'] = new_password
                updated = True
        return updated, sources[0]['sources']


class SecretsRepository(PasswordGenerationVariablesRepositoryInterface):
    """Repository layer to save values which are used with password logic"""
    def __init__(self, table_name):
        super().__init__(table_name)
        self.env_vars = self._initiate_db_connection()
        self.metadata.create_all(self.engine, checkfirst=True)

    def save_value(self, entry: PasswordAddValuesDTO) -> bool:
        self.logging.debug(f"About to save secret for {entry.username}")
        success = True
        if entry is not None and len(entry.username) and len(entry.value) and len(entry.key):
            existing_value = self.get_value(PasswordValuesDTO(entry.username, entry.key))
            # We do not wish to save the same value for user twice
            if existing_value:  # If value exists we update it
                query = update(self.env_vars).values(
                    value=entry.value,
                    created_at=datetime.datetime.now()
                ).where(self.env_vars.columns.username == entry.username).where(
                    self.env_vars.columns.var_key == entry.key)
            else:  # Adding a new value if one does not exist
                query = insert(self.env_vars).values(
                    username=entry.username,
                    var_key=entry.key,
                    value=entry.value,
                    created_at=datetime.datetime.now()
                )
            self.logging.debug(f'Query to be executed {query}')
            with self.engine.begin() as conn:
                try:
                    conn.execute(query)
                except Exception as ex:
                    self.logging.error(f'Error: while saving value for {entry.username} {ex}')
                    success = False
        else:
            success = False
        self.logging.debug(f"Logging was {'successful' if success else 'unsuccessful'}")
        return success

    def get_value(self, entry: PasswordValuesDTO):
        self.logging.debug(f'About to retrieve {entry.username}')
        found_value = None
        if entry is not None and len(entry.username) and len(entry.key):
            query = select(self.env_vars.columns.value).where(self.env_vars.columns.username == entry.username).where(
                self.env_vars.columns.var_key == entry.key)
            try:
                with self.engine.begin() as conn:
                    found_value = conn.execute(query).fetchone()
                    found_value = found_value[0] if found_value is not None else None
            except Exception as ex:
                self.logging.error(f'Unknown error: {ex}')
        return found_value

    def _initiate_db_connection(self):
        return db.Table(
            self.table,
            self.metadata,
            db.Column('env_var_id', db.Integer, Sequence('env_var_seq'), primary_key=True, nullable=False),
            db.Column('username', db.String(16), nullable=False),
            db.Column('var_key', db.String(16), nullable=False),
            db.Column('value', db.BLOB(64), nullable=False),
            db.Column('created_at', db.DateTime, nullable=False)
        )
