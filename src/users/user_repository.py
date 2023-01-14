import datetime
import logging
import time

import sqlalchemy as db
from sqlalchemy import Sequence, insert, select, delete
from sqlalchemy.exc import DatabaseError

from src.interface.repository import UserSQLRepositoryInterface
from src.users.user_dto import UserSaveDTO, UserGetDTO


class UserRepository(UserSQLRepositoryInterface):

    def __init__(self, table_name):
        super().__init__(table_name)
        self.user_tables = self._initiate_db_connection()
        self.metadata.create_all(self.engine, checkfirst=True)

    def find_user_by_username(self, username) -> UserGetDTO:
        self.logging.debug(f'Looking form user {username}')
        response = None
        user_dto = None
        query = select(
            self.user_tables.columns.username,
            self.user_tables.columns.master_password,
            self.user_tables.columns.created_at
        ).where(self.user_tables.columns.username==username)
        try:
            with self.engine.begin() as conn:
                response = conn.execute(query).fetchone()
        except DatabaseError as de:
            self.logging.error(f'Error: {de}')
        except Exception as ex:
            self.logging.error(f'Unknown error: {ex}')

        if response is not None:
            user_dto = UserGetDTO(*response)
            self.logging.debug(f'User {user_dto.username} was fetched from the DB')
        else:
            self.logging.debug(f'Did not find user {username}')
        return user_dto

    def create_user(self, user: UserSaveDTO) -> bool:
        self.logging.debug(f'Saving user {user.username}')
        success = True
        query = insert(self.user_tables).values(username = user.username,
                                                master_password = user.master_password,
                                                created_at=datetime.datetime.now())
        self.logging.debug(f'Query to be executed {query}')
        with self.engine.begin() as conn:
            try:
                conn.execute(query)
            except Exception as ex:
                self.logging.error(f'Error: while saving user {user.username} {ex}')
                success = False
        self.logging.debug(f"Created user {user.username}")
        return success

    def delete_user_by_username(self, username) -> bool:
        self.logging.debug(f'Deleting user {username}')
        success = True
        query = delete(self.user_tables).where(
            self.user_tables.columns.username==username
        )
        with self.engine.begin() as conn:
            try:
                conn.execute(query)
            except Exception as ex:
                logging.error(f'Error: {ex} while deleting {username}')
                success = False
        return success

    def _drop_table(self):
        self.logging.debug(f'Dropping table {self.table}')
        self.user_tables.drop(self.engine)

    def _initiate_db_connection(self):
            return db.Table(
                self.table,
                self.metadata,
                db.Column('user_id', db.Integer, Sequence('user_id_seq'),primary_key=True, nullable=False),
                db.Column('username', db.String(16), unique=True, nullable=False),
                db.Column('master_password', db.String(256), nullable=False),
                db.Column('created_at', db.DateTime, nullable=False),
            )

