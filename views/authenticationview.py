"""Authentication view"""

from utils import Utils


class AuthenticationView:
    CHOICES = ["u", "c", "e", "cl", "q"]

    def __init__(self):
        self.utils = Utils()

    def ask_authentication(self):
        print("Bienvenue dans le menu d'authentification\n")
        login = self.utils.information_menu(
            asking_sentence="Veuillez entrer votre identifiant", in_lower=False
        )
        if not login:
            return None
        password = self.utils.information_menu(
            asking_sentence="Veuillez entrer votre mot de passe", in_lower=False
        )
        if not password:
            return None
        authentication_data = [login, password]
        return authentication_data

    def add_new_password(self, last_password):
        """New User view. This view is used to define a
        new personal password in first loggin."""
        while True:
            password = input(
                "Vous ne vous êtes jamais connecté auparavant. "
                + "Vous devez créer un nouveau mot de passe.\n> "
            )
            if len(password) < 8:
                self.utils.display_red_message("Votre mot de passe est trop court")
                continue
            elif password == last_password:
                self.utils.display_red_message(
                    "Votre mot de passe ne doit pas être identique"
                )
            password_confirm = input("Entrer de nouveau votre mot de passe\n> ")
            if password == password_confirm:
                return password
            else:
                self.utils.display_red_message("Votre mot de passe ne correspond pas")

    def select_menu_by_role(self, user):
        role = user.role.value
        choice_option = {}
        if role == "Saleperson":
            choice_option = {
                "c": "La gestion des contrats",
                "e": "La gestion des évenements",
                "cl": "La gestions des clients",
            }
        elif role == "Manager":
            choice_option = {
                "u": "La gestion des collaborateurs",
                "c": "La gestion des contrats",
                "e": "La gestion des évenements",
                "cl": "L'affichage des clients",
            }
        elif role == "Support":
            choice_option = {
                "c": "L'affichage des contrats",
                "e": "La gestion des évenements",
                "cl": "L'affichage des clients",
            }
        else:
            return None
        choice = self.utils.create_menu(choice_option)
        if choice in self.CHOICES:
            return choice
        else:
            return None
