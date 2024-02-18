"""Authentication controller"""

from views.authenticationview import AuthenticationView
from models.user import User
from utils import Utils


class AuthenticationController:
    def __init__(self, session):
        self.view = AuthenticationView()
        self.user = User(session)
        self.utils = Utils()

    def authenticate(self):
        authentication_request = self.view.ask_authentication()
        if authentication_request:
            user_authenticate = self.user.search_user(
                authentication_request[0], authentication_request[1]
            )
            if user_authenticate:
                # In database, True = 1 and False = 0
                if user_authenticate.first_using_password is True:
                    new_password = self.view.add_new_password(
                        user_authenticate.password
                    )
                    user_authenticate.password = new_password
                    user_authenticate.first_using_password = False
                    update = self.user.update_user(user_authenticate)
                    if update:
                        self.utils.display_green_message(
                            "Mot de passe changer.\nAccès autorisé"
                        )
                        return user_authenticate
                    else:
                        self.utils.display_red_message(
                            "Une erreur s'est produite.\n"
                            + " Vos modifications n'ont pas "
                            + "été prise en compte."
                        )
                        return None
                elif user_authenticate.first_using_password is False:
                    self.utils.display_green_message("Accès autorisé")
                    return user_authenticate
            else:
                self.utils.display_red_message(
                    "Accès non autorisé, les informations ne sont pas "
                    + "présentes dans la base de donnée."
                )
                return None
        else:
            self.utils.display_red_message("Vous quittez le programme.")
            return None

    def main_menu(self, user):
        if user:
            self.utils.display_green_message(f"Bonjour, {user.complete_name}")
            selection = self.view.select_menu_by_role(user)
            return selection
        else:
            return None
