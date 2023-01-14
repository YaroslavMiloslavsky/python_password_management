
class GlobalConfiguration:

    @staticmethod
    def get_tables():
        return {
            'secrets': 'global_vars',
            'users': 'app_users',
            'passwords': 'user_passwords'
        }