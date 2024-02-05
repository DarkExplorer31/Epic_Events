"""Authentication controller"""

from views.authenticationview import AuthenticationView

TRY_DATA = [("user", "password"), ("try", "trypassword")]


class AuthenticationController:
    def __init__(self):
        self.view = AuthenticationView()
        self.view.set_controller(self)
        self.view.run()

    def authenticate(self, username, password):
        if not username:
            self.view.display_error("Votre nom d'utilisateur ne peut pas être vide")
        elif not password:
            self.view.display_error("Votre mot de passe ne peut pas être vide")
        elif (username, password) in TRY_DATA:
            self.view.close()
        else:
            self.view.display_error("Vos identifiants sont incorrectes")
