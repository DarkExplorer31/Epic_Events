"""Authentication controller"""

from views.authenticationview import AuthenticationView
from models.user import User


class AuthenticationController:
    def __init__(self, session):
        self.view = AuthenticationView()
        self.user = User()
        self.session = session

    def authenticate(self):
        """"""
        authentication_request = self.view.ask_authentication()
        if not authentication_request[1]:
            user = (
                self.session.query(User)
                .filter(User.email == authentication_request[0])
                .first()
            )
            if user.password:
                self.view.display_message(
                    "Accès non autorisé, les informations ne sont pas "
                    + "présentes dans la base de donnée."
                )
                return None
            else:
                new_password = self.view.add_new_password()
                user.password = new_password
                self.session.add(user)
                self.session.commit()
                self.view.display_message("Accès autorisé")
                return user
        if authentication_request:
            authentication_db = (
                self.session.query(User)
                .filter(
                    User.email == authentication_request[0],
                    User.password == authentication_request[1],
                )
                .first()
            )
            if authentication_db:
                self.view.display_message("Accès autorisé")
                return authentication_db
            else:
                self.view.display_message(
                    "Accès non autorisé, les informations ne sont pas"
                    + " présentes dans la base de donnée."
                )
                return None
        else:
            self.view.display_message(
                "Accès non autorisé, les informations ne sont pas "
                + "présentes dans la base de donnée."
            )
            return None

    def main_menu(self):
        """Display menu options based on user role"""
        connected = self.authenticate()
        if connected:
            selected_menu = self.view.select_menu_by_role(connected.role)
            if selected_menu:
                return selected_menu
        else:
            return None
