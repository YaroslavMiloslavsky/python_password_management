from src.usif.usif_impl import UserSimpleInterFace
from src.utils.global_utils import GlobalConfiguration


class LogicLoop:

    def __init__(self):
        self.interaction = UserSimpleInterFace(
            password_table=GlobalConfiguration.get_tables()['passwords']
        )

    def so_it_has_begun(self):
        while True:
            # if self.interaction.current_auth.auth is False:
            if self.interaction.current_session.auth is False:
                interaction = self.interaction.interact()
                if interaction == 'l':
                    self.interaction.login()
                elif interaction == 's':
                    self.interaction.signup()
                elif interaction == 'e':
                    self.interaction.exit()
                else:
                    continue
            else:
                interaction = self.interaction.interact()
                if interaction == 'a':
                    self.interaction.add_new_password()
                elif interaction == 'u':
                    self.interaction.use()
                elif interaction == 'b':
                    self.interaction.current_session.auth = False
                else:
                    continue