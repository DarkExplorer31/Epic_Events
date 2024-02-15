"""Authentication view"""

from utils import Utils


class AuthenticationView:
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

    def display_message(self, message):
        print(message)

    def select_menu_by_role(self, role):
        if role == "Sales":
            pass
        elif role == "Manager":
            choice_option = {
                "'u'": "La gestion des collaborateurs",
                "'c'": "La gestion des contrats",
                "'e'": "La gestion des évenements",
            }
            choice = self.utils.create_menu(choice_option)
            if choice in ["u", "c", "e", "q"]:
                return choice
            else:
                print("Votre demande n'est pas comprise.")
                return None
        elif role == "Support":
            pass
