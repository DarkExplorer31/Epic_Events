"""User view"""

from utils import Menu, display_green_message, display_red_message, generate_password


class UserView:
    ROLE = ["Sales", "Manager", "Support"]
    EMAIL_TYPE = "@"

    def __init__(self):
        self.menu = Menu()

    # Displaying methods
    def display_users(self, users):
        if users:
            for user in users:
                print(f"-{user}")
        else:
            display_red_message("Votre liste d'utilisateur actuel est vide.\n")

    def display_roles(self):
        print("Les roles qui peuvent être: ")
        for role in self.ROLE:
            print(f"-{role}")
        print("\n")

    def display_created(self):
        display_green_message("L'utilisateur a été créé.")

    def display_not_created(self):
        display_red_message("L'utilisateur n'a pas été créé.")

    def display_unfound_user(self):
        display_red_message("L'utilisateur n'a pas été trouvé.")

    def display_selected_user(self, user):
        print(
            f"Vous avez sélectionné l'utilisateur : {user.email}."
            + "\nVous ne pourrez changer que le rôle, le nom complet"
            + " ou le numéro de téléphone.\n"
            + f" Actuellement, son rôle est : {user.role}.\n"
            + f"Le numéro de téléphone est : {user.phone_number}.\n"
            + f"Et le nom complet : {user.complete_name}.\n\n"
        )

    def display_user_is_update(self):
        display_green_message("L'utilisateur a été mis à jour.")

    def display_user_is_not_update(self):
        display_red_message("L'utilisateur n'a pas été mis à jour.")

    def display_user_is_delete(self):
        display_green_message("L'utilisateur a été supprimé.")

    def display_user_is_not_delete(self):
        display_red_message("L'utilisateur n'a pas été supprimé.")

    def display_user_is_not_authorized(self):
        display_red_message("Vous n'avez pas le droit d'accéder à ces fonctionnalités.")

    # Other methods
    def get_new_user_information(self):
        print("Bienvenue dans la création d'un nouveau collaborateur\n")
        self.display_roles()
        while True:
            role = self.menu.information_menu(
                asking_sentence="Veuillez remplir son nouveau rôle",
                possible_response=self.ROLE,
                not_conform_message="Le role doit être: Sales, Management ou Support",
            )
            if not role:
                return None
            complete_name = self.menu.information_menu(
                asking_sentence="Veuillez remplir son nom complet"
            )
            if not complete_name:
                return None
            email = self.menu.information_menu(
                asking_sentence="Veuillez remplir son email",
                value_in_sentence=self.EMAIL_TYPE,
                not_conform_message="L'email doit comporter un '@'",
            )
            if not email:
                return None
            phone_number = self.menu.information_menu(
                asking_sentence="Veuillez remplir son numéro de tel."
            )
            if not phone_number:
                return None
            print(
                "La demande d'inscription à été prise en compte. Ce nouvelle"
                + " utilisateur devra entré un nouveau mot de "
                + "passe dès sa première connexion"
            )
            password = generate_password()
            return {
                "role": role,
                "complete_name": complete_name,
                "email": email,
                "phone_number": phone_number,
                "password": password,
            }

    def search_user(self):
        print("Bienvenue dans la fonction de recherche d'un collaborateur")
        email = self.menu.information_menu(
            asking_sentence="Veuillez remplir son email",
            value_in_sentence=self.EMAIL_TYPE,
            not_conform_message="L'email doit comporter un '@'",
        )
        return email

    def get_update_user_informations(self, user):
        self.display_selected_user(user)
        role = self.menu.information_menu(
            asking_sentence="Veuillez remplir son nouveau rôle",
            possible_response=self.ROLE,
            not_conform_message="Le role doit être :Sales, Management ou Support",
        )
        if not role:
            display_red_message("Le role n'a pas été changer")
        else:
            user.role = role.upper()
            display_green_message("Le role à été changer.")
        complete_name = self.menu.information_menu(
            asking_sentence="Veuillez remplir son nom complet"
        )
        if not complete_name:
            display_red_message("Le nom n'a pas été changer")
        else:
            user.complete_name = complete_name
            display_green_message("Le nom à été changer.")
        phone_number = self.menu.information_menu(
            asking_sentence="Veuillez remplir son numéro de tel."
        )
        if not phone_number:
            display_red_message("Le numéro de téléphone n'a pas été changer")
        else:
            user.phone_number = phone_number
            display_green_message("Le numéro de téléphone à été changer.")
        return user

    def choice_menu(self):
        choice = self.menu.crud_menu("utilisateur")
        return choice
