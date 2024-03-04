"""Authentication view"""

import getpass
from utils import Menu, display_red_message, display_green_message


class AuthenticationView:
    CHOICES = ["u", "c", "e", "cl", "q"]

    def __init__(self):
        self.menu = Menu()

    # Display specific messages:
    def display_quit(self):
        display_red_message("Vous quittez le programme.")

    def display_acces_non_autorise(self):
        display_red_message(
            "Les identifiants fournis sont incorrects.\nAccès non autorisé"
        )

    def display_acces_autorise(self):
        display_green_message("Accès autorisé")

    def display_password_changed(self):
        display_green_message("Mot de passe changé.\nAccès autorisé")

    def display_unchange_password(self):
        display_red_message(
            "Une erreur s'est produite.\n"
            + " Vos modifications n'ont pas "
            + "été prises en compte."
        )

    def display_hello_user(self, user):
        display_green_message(f"Bonjour, {user.complete_name}")

    # Asking user information:
    def ask_authentication(self):
        print("Bienvenue dans le menu d'authentification\n")
        login = self.menu.information_menu(
            asking_sentence="Veuillez entrer votre identifiant"
        )
        if not login:
            return None
        password = getpass.getpass("Veuillez entrer votre mot de passe:\n>")
        if not password:
            return None
        return {"login": login, "password": password}

    def add_new_password(self, last_password):
        """New User view. This view is used to define a
        new personal password on first login."""
        while True:
            password = getpass.getpass(
                "Vous ne vous êtes jamais connecté auparavant. "
                + "Vous devez créer un nouveau mot de passe.\n> "
            )
            if len(password) < 8:
                display_red_message("Votre mot de passe est trop court")
                continue
            elif password == last_password:
                display_red_message("Votre mot de passe ne doit pas être identique")
            password_confirm = getpass.getpass(
                "Entrez à nouveau votre mot de passe\n> "
            )
            if password == password_confirm:
                return password
            else:
                display_red_message("Votre mot de passe ne correspond pas")

    def select_menu_by_role(self, user):
        role = user.role.value
        choice_option = {}
        if role == "Sales":
            choice_option = {
                "c": "La gestion des contrats",
                "e": "La gestion des événements",
                "cl": "La gestion des clients",
            }
        elif role == "Manager":
            choice_option = {
                "u": "La gestion des collaborateurs",
                "c": "La gestion des contrats",
                "e": "La gestion des événements",
                "cl": "L'affichage des clients",
            }
        elif role == "Support":
            choice_option = {
                "c": "L'affichage des contrats",
                "e": "La gestion des événements",
                "cl": "L'affichage des clients",
            }
        choice = self.menu.global_menu(choice_option)
        if choice in self.CHOICES:
            return choice
