"""User view"""

from utils import Utils


class UserView:
    ROLE = ["Sales", "Manager", "Support"]
    EMAIL_TYPE = "@"

    def __init__(self):
        self.utils = Utils()

    def display_users(self, all_users):
        for user in all_users:
            print(f"-{user}")
        self.utils.display_green_message("La liste est terminer.\n")

    def add_new_user_view(self, username):
        """Manager view, ask role, complete_name, email and phone_number
        to create a new User in db. The password is generated and not asking."""
        print(
            f"Bienvenue dans la création d'un nouveau collaborateur {username}" + "\n"
        )
        print("Les roles qui peuvent être: ")
        for role in self.ROLE:
            print(f"-{role}")
        print("\n")
        while True:
            role = self.utils.information_menu(
                asking_sentence="Veuillez remplir son nouveau rôle",
                constant=self.ROLE,
                not_in_constant_message="Le role doit être: Sales, Management ou Support",
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
                reverse_constant=self.EMAIL_TYPE,
                not_in_constant_message="L'email doit comporter un '@'",
            )
            if not email:
                return None
            phone_number = self.utils.information_menu(
                asking_sentence="Veuillez remplir son numéro de tel."
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

    def find_user(self):
        print(f"Bienvenue dans la fonction de recherche d'un collaborateur")
        email = input(
            "Veuillez saisir l'email du collaborateur à mettre à jour ou 'q' pour quitter\n> "
        )
        if email:
            return email
        else:
            return None

    def update_user_information_view(self, user):
        """Manager view, ask role, complete_name and phone_number
        to update User in db."""
        print(
            "\n"
            + f"Vous voulez mettre à jour les information de {user.email}."
            + "\nVous ne pourrait changer que le role,"
            + " le nom complet ou le numéro de téléphone."
            + f"Actuellement, son role est: {user.role}"
            + "\n"
            + f"le numéro de téléphone est: {user.phone_number}"
            + "\n"
            + f"et le nom complet: {user.complete_name}"
            + "\n"
        )
        role = self.utils.information_menu(
            asking_sentence="Veuillez remplir son nouveau rôle",
            constant=self.ROLE,
            not_in_constant_message="Le role doit être :Sales, Management ou Support",
        )
        if not role:
            self.utils.display_red_message("Le role n'a pas été changer")
        else:
            user.role = role
            self.utils.display_green_message("Le role à été changer.")
        complete_name = self.utils.information_menu(
            asking_sentence="Veuillez remplir son nom complet"
        )
        if not complete_name:
            self.utils.display_red_message("Le nom n'a pas été changer")
        else:
            user.complete_name = complete_name
            self.utils.display_green_message("Le nom à été changer.")
        phone_number = self.utils.information_menu(
            asking_sentence="Veuillez remplir son numéro de tel."
        )
        if not phone_number:
            self.utils.display_red_message("Le numéro de téléphone n'a pas été changer")
        else:
            user.phone_number = phone_number
            self.utils.display_green_message("Le numéro de téléphone à été changer.")
        return user

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

    def confirm_choice(self, user_to_delete):
        confirmation = ""
        while confirmation != "q":
            confirmation = self.utils.information_menu(
                asking_sentence="êtes-vous sûr de vouloir supprimer "
                + f"l'utilisateur '{user_to_delete.complete_name}' (y/n)"
            )
            if confirmation == "y":
                return True
            elif confirmation == "n" or confirmation == "q":
                return False
            else:
                continue

    def display_information(self, user_save, succes_message, error_message):
        if user_save is True:
            self.utils.display_green_message(f"{succes_message}")
        else:
            self.utils.display_red_message(f"{error_message}")

    def user_menu(self):
        menu_options = {
            "t": "Voir tout les utilisateurs",
            "a": "Ajoutez un utilisateur",
            "u": "Mettez à jour un utilisateur",
            "d": "Supprimez un utilisateur",
        }
        menu = self.utils.create_menu(options=menu_options)
        if menu == "q":
            return None
        else:
            return menu
