class AuthServiceInterface:
    def __init__(self):
        self.auth = False
        self.username = None
        self.password = None

    def auth_user(self):
        """Auth the user"""
        pass

    def register_new_user(self):
        """Registers new user"""
        pass