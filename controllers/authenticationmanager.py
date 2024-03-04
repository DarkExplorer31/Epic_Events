"""Authentication controller"""

from views.authenticationview import AuthenticationView
from models.usermodel import UserModel


class AuthenticationController:
    def __init__(self, session):
        self.view = AuthenticationView()
        self.user = UserModel(session)

    def authenticate(self):
        authentication_request = self.view.ask_authentication()
        if not authentication_request:
            self.view.display_quit()
            return None
        user_authenticate = self.user.search(
            authentication_request["login"], authentication_request["password"]
        )
        if not user_authenticate:
            self.view.display_acces_non_autorise()
            return None
        # In database, True = 1 and False = 0
        if user_authenticate.first_using_password is True:
            new_password = self.view.add_new_password(user_authenticate.password)
            update = self.user.change_password(user_authenticate.id, new_password)
            if not update:
                self.view.display_unchange_password()
                return None
            self.view.display_password_changed()
            return user_authenticate
        self.view.display_acces_autorise()
        return user_authenticate

    def main_menu(self, user):
        self.view.display_hello_user(user)
        return self.view.select_menu_by_role(user)
