"""Client view"""

from utils import Menu, display_green_message, display_red_message


class ClientView:
    EMAIL_TYPE = "@"

    def __init__(self):
        self.menu = Menu()

    # Displaying methods
    def display_clients(self, clients):
        if clients:
            display_green_message("Voici la liste des clients actuels:\n")
            for client in clients:
                print(f"-{client}")
        else:
            display_red_message("Votre liste de client actuel est vide.\n")

    def display_created(self):
        display_green_message("Le client a été créé.")

    def display_not_created(self):
        display_red_message(
            "Le client n'a pas été créé."
            + " Veuillez vérifier que l'email "
            + "ou le numéro de téléphone sont bien uniques."
        )

    def display_unfound_client(self):
        display_red_message("Le client n'a pas été trouvé.")

    def display_selected_client(self, client):
        print(
            "\n"
            + f"Vous voulez mettre à jour les informations de {client.company_name}."
            + "\n"
            + f"Actuellement, le contact est: {client.email}"
            + "\n"
            + f"le numéro de téléphone est: {client.phone_number}"
            + "\n"
            + f"le nom complet du contact: {client.complete_name}"
            + "\n"
            + f"et le nom de l'entreprise est: {client.company_name}"
        )

    def display_client_is_not_under_responsibility(self):
        display_red_message("Le client n'est pas sous votre responsabilité.")

    def display_client_is_update(self):
        display_green_message("Le client a été mis à jour.")

    def display_client_is_not_update(self):
        display_red_message(
            "Le client n'a pas été mis à jour."
            + " Veuillez vérifier que l'email "
            + "ou le numéro de téléphone sont bien uniques."
        )

    def display_client_is_delete(self):
        display_green_message("Le client a été supprimé.")

    def display_client_is_not_delete(self):
        display_red_message("Le client n'a pas été supprimé.")

    def display_not_authorized(self):
        display_red_message("Vous n'avez pas le droit d'accéder à ces fonctionnalités.")

    # Other methods
    def get_new_client_information(self):
        print("Bienvenue dans la création d'un nouveau client\n")
        while True:
            complete_name = self.menu.information_menu(
                asking_sentence="Veuillez remplir le nom complet du contact client"
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
            company_name = self.menu.information_menu(
                asking_sentence="Veuillez remplir le nom de la compagnie"
            )
            if not company_name:
                return None
            return {
                "complete_name": complete_name,
                "email": email,
                "phone_number": phone_number,
                "company_name": company_name,
            }

    def search_client(self):
        print("Bienvenue dans la fonction de recherche d'un client")
        email = self.menu.information_menu(
            asking_sentence="Veuillez remplir son email",
            value_in_sentence=self.EMAIL_TYPE,
            not_conform_message="L'email doit comporter un '@'",
        )
        return email

    def get_update_client_informations(self, client):
        self.display_selected_client(client)
        complete_name = self.menu.information_menu(
            asking_sentence="Veuillez remplir le nom complet du contact client"
        )
        if not complete_name:
            display_red_message("Le nom n'a pas été changer")
        else:
            client.complete_name = complete_name
            display_green_message("Le nom à été changer.")
        email = self.menu.information_menu(
            asking_sentence="Veuillez remplir son email",
            value_in_sentence=self.EMAIL_TYPE,
            not_conform_message="L'email doit comporter un '@'",
        )
        if not email:
            display_red_message("L'email' n'a pas été changer")
        else:
            client.email = email
            display_green_message("L'email à été changer.")
        phone_number = self.menu.information_menu(
            asking_sentence="Veuillez remplir son numéro de tel."
        )
        if not phone_number:
            display_red_message("Le numéro de téléphone n'a pas été changer")
        else:
            client.phone_number = phone_number
            display_green_message("Le numéro de téléphone à été changer.")
        company_name = self.menu.information_menu(
            asking_sentence="Veuillez remplir le nom de la compagnie"
        )
        if not company_name:
            display_red_message("Le numéro de téléphone n'a pas été changer")
        else:
            client.company_name = company_name
            display_green_message("Le nom de l'entreprise à été changer.")
        return client

    def delete_confirmation(self, client_email):
        return self.menu.confirm_choice(client_email)

    def choice_menu(self, user_role):
        if user_role == "Sales":
            choice = self.menu.crud_menu("client")
        else:
            choice = self.menu.no_permission_menu("client")
        return choice
