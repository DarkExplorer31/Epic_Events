"""User view"""

from utils import Menu, display_green_message, display_red_message, generate_password


class UserView:
    ROLE = ["Sales", "Manager", "Support"]
    EMAIL_TYPE = "@"

    def __init__(self):
        self.menu = Menu()

    def display_users(self, all_users):
        for user in all_users:
            print(f"-{user}")
        display_green_message("La liste est terminer.\n")

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
        role = self.menu.information_menu(
            asking_sentence="Veuillez remplir son nouveau rôle",
            possible_response=self.ROLE,
            not_conform_message="Le role doit être :Sales, Management ou Support",
        )
        if not role:
            display_red_message("Le role n'a pas été changer")
        else:
            user.role = role
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

    def display_management_menu(self, username):
        """Manager view, used to display a menu to User with 'Manager' role."""
        print(f"Bienvenu {username}")
        options = {
            "c": "créer un nouvel utilistateur",
            "u": " mettre à jour un utilisateur",
            "d": " suprimer un utilisateur",
        }
        choice = self.menu.global_menu(options)
        return choice


    def user_menu(self):
        menu_options = {
            "t": "Voir tout les utilisateurs",
            "a": "Ajoutez un utilisateur",
            "u": "Mettez à jour un utilisateur",
            "d": "Supprimez un utilisateur",
        }
        menu = self.menu.global_menu(options=menu_options)
        if menu == "q":
            return None
        else:
            return menu
