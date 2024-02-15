"""User view"""

from utils import Utils

ROLE = ["Sales", "Management", "Support"]
EMAIL_TYPE = "@"


class UserView:
    def __init__(self):
        self.utils = Utils()

    def add_new_password(self):
        """New User view. This view is used to define a
        new personal password in first loggin."""
        while True:
            password = input("Votre mot de passe est vide. Vous devez en créer un.\n> ")
            if len(password) < 8:
                print("Votre mot de passe est trop court")
                continue
            password_confirm = input("Entrer de nouveau votre mot de passe\n> ")
            if password == password_confirm:
                return password
            else:
                print("Votre mot de passe ne correspond pas")

    def add_new_user_view(self, username):
        """Manager view, ask role, complete_name, email and phone_number
        to create a new User in db. The password is generated and not asking."""
        while True:
            print(f"Bienvenue dans la création d'un nouveau collaborateur {username}")
            role = self.utils.information_menu(
                asking_sentence="Veuillez remplir son nouveau rôle",
                constant=ROLE,
                not_in_constant_message="Le role doit être :Sales, Management ou Support",
            )
            if not role:
                return None
            complete_name = self.utils.information_menu(
                asking_sentence="Veuillez remplir son nom complet"
            )
            if not complete_name:
                return None
            email = self.utils.information_menu(
                asking_sentence="Veuillez remplir son email",
                reverse_constant=EMAIL_TYPE,
                not_in_constant_message="L'email doit comporter un '@'",
            )
            if not email:
                return None
            phone_number = self.utils.information_menu(
                asking_sentence="Veuillez remplir son numéro de tel.", in_lower=False
            )
            if not phone_number:
                return None
            print(
                "La demande d'inscription à été prise en compte. Ce nouvelle"
                + " utilisateur devra entré un nouveau mot de "
                + "passe dès sa première connexion"
            )
            password = self.utils.generate_password()
            return [role, complete_name, email, phone_number, password]

    def display_management_menu(self, username):
        """Manager view, used to display a menu to User with 'Manager' role."""
        print(f"Bienvenu {username}")
        options = {
            "c": "créer un nouvel utilistateur",
            "u": " mettre à jour un utilisateur",
            "d": " suprimer un utilisateur",
        }
        choice = self.utils.create_menu(options)
        return choice
