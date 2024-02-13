"""Authentication controller"""

from views.userview import UserView
from models.user import User


class AuthenticationController:
    def __init__(self, session):
        self.view = UserView()
        self.user = User()
        self.session = session

    def authenticate(self):
        authentication_request = self.view.ask_authentication()
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
                return True
            else:
                self.view.display_message(
                    "Accès non autorisé, les informations ne sont pas"
                    + " présentes dans la base de donnée."
                )
                return False
        else:
            self.view.display_message(
                "Accès non autorisé, les informations ne sont pas "
                + "présentes dans la base de donnée."
            )
            return False
