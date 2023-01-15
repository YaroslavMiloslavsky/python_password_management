import os
import time

import maskpass
import pyperclip

from src.interface.usif import UsifInterface
from src.password.pwd_dto import PasswordNewEntry
from src.password.pwd_repository import PasswordRepository
from src.users.session_service import SessionService
from src.utils.global_utils import GlobalConfiguration
from src.utils.hashing_utils import HashingUtils
from src.utils.value_generation_util import ValueGenerator


class UserSimpleInterFace(UsifInterface):
    def __init__(self, password_table):
        super().__init__()
        self.os_name = os.name
        self.current_session = SessionService(secret_table=GlobalConfiguration.get_tables()['secrets'],
                                              user_table=GlobalConfiguration.get_tables()['users'])
        self.password_repository = PasswordRepository(password_table)


    def interact(self):
        self._clear()
        if not self.current_session.auth:
            print('Not Auth')
            self._interact_not_auth()
        else:
            print('Yes Auth')
            self._interact_auth()
        user_selection = str(input())
        return user_selection[0].lower() if len(user_selection) > 0 else ''

    def login(self) -> bool:
        self._clear()
        username = str(input('Please enter username: '))
        password = maskpass.askpass(mask='*')
        self.current_session.set_current_user(username, password)
        self.current_session.auth_user()
        return self.current_session.auth

    def signup(self) -> bool:
        self._clear()
        print("Glad to hear you wish to join our service")
        username = str(input('Please chose username: '))
        password = maskpass.askpass(mask='*')
        if len(username) > 0 and password is not None and len(password) > 0:
            self.current_session.set_current_user(username, password)
            self.password_repository.save(PasswordNewEntry(
                username=self.current_session.username
            ))
            self.current_session.register_new_user()
        else:
            print("Please don't use these credentials")
            time.sleep(1)
        return self.current_session.auth

    def _clear(self):
        os.system('cls' if self.os_name == 'nt' else 'clear')

    def exit(self):
        print('Goodbye...')
        self.current_session.auth = False
        time.sleep(2)
        self._clear()
        exit()

    def _show_all_entries(self):
        entries = self.password_repository.get_all(self.current_session.username)
        if len(entries) > 0:
            for entry in entries:
                password = HashingUtils.un_hash_value(
                    value=entry["source_pwd"],
                    secret=self.current_session.password_service.get_key(self.current_session.username),
                    salt=self.current_session.password_service.get_salt(self.current_session.username)
                )
                print('-------------------------------')
                print(
                    f'App:      {entry["source_name"]}\n'
                    f'Username: {entry["source_username"]}\n'
                    f'Password: {password}'
                )
                print('-------------------------------')
        else:
            print('No saved entries, care to expand the list?')

    def _interact_not_auth(self):
        print(f'Hello {self.current_session.username if self.current_session.username is not None else "human being"}!')
        print('Please select an option')
        print('(L)ogin')
        print('(S)ign Up')
        print('(E)xit')

    def _interact_auth(self):
        print(f'Hello {self.current_session.username}')
        print('Do you wish to:')
        print('(U)se')
        print('(A)dd')
        print('(B)ack')

    def use(self):
        self._clear()
        print('You passwords:')
        self._show_all_entries()
        action = str(input('User password for source name: '))
        if len(action) > 0:
            selected = self.password_repository.get(action, self.current_session.username)
            selected_password = selected[1].sources[0]['source_pwd']
            selected_password = HashingUtils.un_hash_value(
                value=selected_password,
                secret=self.current_session.password_service.get_key(self.current_session.username),
                salt=self.current_session.password_service.get_salt(self.current_session.username)
            )
            pyperclip.copy(selected_password)
        else:
            print('No such source.. but you know that')
            time.sleep(1)

    def add_new_password(self):
        self._clear()
        password = None
        print('(C)reate')
        print('(G)enerate')
        action = str(input('Please choose an option: '))
        if len(action) == 0:
            return
        if action[0].lower() == 'g':
            length = int(input('Please enter length: '))
            password = ValueGenerator.generate_password(length)
        elif action[0].lower() == 'c':
            password = str(input('Please enter a new password: '))
        else:
            print('What?')
            time.sleep(1)

        password_username = str(input('Please enter a username for this password: '))
        object_name = str(input('Please choose the subject for this: '))

        if len(password_username) or len(object_name):
            return

        hashed_pwd = HashingUtils.hash_value(
            value=password,
            secret=self.current_session.password_service.get_key(self.current_session.username),
            salt=self.current_session.password_service.get_salt(self.current_session.username)
        )
        self.password_repository.update(
            username=self.current_session.username,
            new_password= hashed_pwd.decode('utf-8'),
            object_name= object_name,
            source_username=password_username
        )
