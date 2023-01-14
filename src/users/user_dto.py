import datetime


class UserDTO:
    """General User DTO class"""
    def __init__(self, username):
        self.username = username

class UserSaveDTO(UserDTO):
    """DTO for saving a user"""
    def __init__(self, username, password):
        super().__init__(username)
        self.master_password = password

class UserGetDTO(UserDTO):
    """DTO for fetching a user"""
    def __init__(self, username, password, created_at):
        super().__init__(username)
        self.master_password = password
        self.created_at = created_at

