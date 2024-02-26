"""Client view"""

from utils import Menu, display_green_message, display_red_message


class ClientView:
    EMAIL_TYPE = "@"

    def __init__(self):
        self.menu = Menu()

    def display_all_clients(self, all_clients):
        if all_clients:
            display_green_message("Voici la liste des clients actuels:\n")
            for client in all_clients:
                print(client)
        else:
            display_red_message("Votre liste de client actuel est vide.\n")

    def add_new_client_view(self):
        print(f"Bienvenue dans la création d'un nouveau client\n")
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
            return [complete_name, email, phone_number, company_name]

    def find_client(self):
        print(f"Bienvenue dans la fonction de recherche d'un client")
        email = self.menu.information_menu(
            asking_sentence="Veuillez remplir son email",
            value_in_sentence=self.EMAIL_TYPE,
            not_conform_message="L'email doit comporter un '@'",
        )
        if not email:
            return None
        else:
            return email

    def update_client_informations_view(self, client):
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
            asking_sentence="Veuillez remplir le nomde la compagnie"
        )
        if not company_name:
            display_red_message("Le numéro de téléphone n'a pas été changer")
        else:
            client.company_name = company_name
            display_green_message("Le nom de l'entreprise à été changer.")
        return client
