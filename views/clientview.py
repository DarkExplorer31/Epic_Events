"""Client View"""

from utils import Menu, display_green_message, display_red_message


class ClientView:
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
        pass
