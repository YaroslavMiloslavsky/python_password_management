import html


class UserInputUtil:
    """Static util library to sanitize and validate the user input"""

    @staticmethod
    def get_threat_symbols():
        """Potential symbols to cause sql injections"""
        return ['=', 'cmd', '(', ')', ';', '|', '&', '^']

    @staticmethod
    def validate_username(username: str) -> (bool,dict):
        """Returns a bool is_valid and reasons the reasons for being invalid
            For example for testUser it will return (False, {})
            But for =cmd(A | 3) it will return (True, {...})"""

        reasons = {}
        valid = True
        if len(username) < 5 or len(username) > 16:
            reasons['length'] = 'Length of username should be no less than 5 and no more than 32'

        html_escaped = html.escape(username)
        if html_escaped != username:
            reasons['symbols'] = 'username contains illegal symbols'

        for symbol in UserInputUtil.get_threat_symbols():
            if symbol in username:
                reasons['hazardous_symbols'] = 'These symbols may pose threat'

        if len(reasons) != 0:
            valid = False
        return valid,reasons

    @staticmethod
    def validate_password(password: str)-> (bool,dict):
        """Validates password, master password should be of length less than 32
            Can be of length less than 5
            Can add more validation if needed
            """
        reasons = {}
        valid = True

        if len(password) < 5 or len(password) > 256:
            reasons['length'] = 'Length of password should be no less than 5 and no more than 256'

        # html_escaped = html.escape(password)
        # if html_escaped != password:
        #     reasons['symbols'] = 'password contains illegal symbols'

        if len(reasons) != 0:
            valid = False
        return valid,reasons