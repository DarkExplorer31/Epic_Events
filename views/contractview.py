"""Contract view"""

from models.db_models import StatusEnum
from utils import Menu, display_green_message, display_red_message


class ContractView:
    STATUS = ["Non signé", "Pas payé", "Payé"]
    EMAIL_TYPE = "@"

    def __init__(self):
        self.menu = Menu()

    # Displaying methods
    def display_contracts(self, contracts):
        if contracts:
            display_green_message("Voici la liste des contracts actuels:\n")
            for contract in contracts:
                print(f"-{contract}")
        else:
            display_red_message("Votre liste de contrat actuel est vide.\n")

    def display_clients_under_responsibility(self, clients):
        if clients:
            display_green_message(
                "Voici la liste des clients qui sont sous votre responsabilité:\n"
            )
            for client in clients:
                print(f"-{client}")
        else:
            display_red_message(
                "Vous n'avez pas de clients sous votre responsabilité,"
                + " vous devez en créer au moins un afin de poursuivre.\n"
            )

    def display_client_is_not_under_responsibility(self):
        display_red_message("Le client n'est pas sous votre responsabilité.")

    def display_unfound_client(self):
        display_red_message("Le client n'a pas été trouvé.")

    def display_created(self):
        display_green_message("Le contrat a été créé.")

    def display_not_created(self):
        display_red_message("Le contrat n'a pas été créé.")

    def display_unfound_contract(self):
        display_red_message("Le contrat n'a pas été trouvé.")

    def display_contract_is_not_under_responsibility(self):
        display_red_message("Le contrat n'est pas sous votre responsabilité.")

    def display_contract_is_update(self):
        display_green_message("Le contrat a été mis à jour.")

    def display_contract_is_not_update(self):
        display_red_message("Le contrat n'a pas été mis à jour.")

    def display_contract_is_delete(self):
        display_green_message("Le contrat a été supprimé.")

    def display_contract_is_not_delete(self):
        display_red_message("Le contrat n'a pas été supprimé.")

    def display_not_authorized(self):
        display_red_message(
            "Vous n'avez pas le droit d'accéder à " + "ces fonctionnalités."
        )

    def display_status(self):
        print("Les statuts qui peuvent être entrés sont: ")
        for choice_status in self.STATUS:
            print(f"-{choice_status}")
        print("\n")

    # Searching methods
    def search_client_under_responsibility(self):
        print("Bienvenue dans la fonction de sélection d'un de vos clients.")
        email = self.menu.information_menu(
            asking_sentence="Veuillez remplir son email",
            value_in_sentence=self.EMAIL_TYPE,
            not_conform_message="L'email doit comporter un '@'",
        )
        return email

    def search_contract(self):
        print("Bienvenue dans la fonction de recherche d'un contrat")
        id = self.menu.information_menu(
            asking_sentence="Veuillez renseigner l'id du contract",
        )
        if not id:
            return None
        try:
            id = int(id)
        except ValueError:
            display_red_message("La valeur attendue est un chiffre.")
            return None
        return id

    # Other methods
    def ask_status(self):
        status = self.menu.information_menu(
            asking_sentence="Veuillez remplir le status actuel du contrat",
            possible_response=self.STATUS,
            not_conform_message="Le status doit être 'Non signé', 'Pas payé' ou 'Payé'",
        )
        if not status:
            return None
        elif status == "Non Payé":
            status = StatusEnum.UNPAID
        elif status == "Non signé":
            status = StatusEnum.UNSIGNED
        elif status == "Payé":
            status = StatusEnum.PAID
        else:
            return None
        return status

    def get_new_contract_information(self):
        print("Bienvenue dans la création d'un nouveau contrat\n")
        while True:
            total_cost = self.menu.information_menu(
                asking_sentence="Veuillez remplir le coût total du contrat"
            )
            if not total_cost:
                return None
            try:
                total_cost = float(total_cost)
            except ValueError:
                display_red_message(
                    "Le format n'est pas bon, ce champ attend un chiffre à virgule."
                )
                continue
            if total_cost < 0.0:
                display_red_message("Le coût ne peut pas être négatif.")
                continue
            elif total_cost == 0.0:
                display_red_message("Le coût ne peut pas être égal à 0.")
                continue
            self.display_status()
            status = self.menu.information_menu(
                asking_sentence="Veuillez remplir le status actuel du contrat",
                possible_response=self.STATUS,
                not_conform_message="Le status doit être 'Non signé', 'Pas payé' ou 'Payé'",
            )
            if not status:
                return None
            if status == "Pas payé":
                status = StatusEnum.UNPAID
                balance = self.menu.information_menu(
                    asking_sentence="Veuillez remplir le coût déjà payé par le client"
                )
                if not balance:
                    return None
                try:
                    balance = float(balance)
                    balance = total_cost - balance
                except ValueError:
                    display_red_message(
                        "Le format n'est pas bon, ce champ attend un chiffre à virgule."
                        + "\nLa balance est définie à hauteur du coût du contrat."
                    )
                    balance = total_cost
                if balance > total_cost or balance < 0.0:
                    display_red_message(
                        "Le prix payé ne peut pas être supérieur au coût"
                        + " du contrat ou inférieur à 0."
                        + "\nLa balance est définie à hauteur"
                        + " du coût du contrat."
                    )
                    balance = total_cost
            elif status == "Non signé":
                status = StatusEnum.UNSIGNED
                balance = total_cost
            elif status == "Payé":
                status = StatusEnum.PAID
                balance = 0.01
            return {"total_cost": total_cost, "balance": balance, "status": status}

    def get_update_contract_informations(self, contract):
        print("Vous voulez mettre à jour:\n" + str(contract))
        self.display_status()
        status = self.menu.information_menu(
            asking_sentence="Veuillez remplir le status actuel du contrat",
            possible_response=self.STATUS,
            not_conform_message="Le status doit être 'Non signé', 'Pas payé' ou 'Payé'",
        )
        if not status:
            return None
        elif status == contract.status:
            display_red_message("Le status n'a pas changé")
        elif status == "Non payé":
            contract.status = StatusEnum.UNPAID
            balance = self.menu.information_menu(
                asking_sentence="Veuillez remplir le coût déjà payé par le client"
            )
            if not balance:
                display_red_message("La balance n'a pas changée")
                return None
            try:
                balance = float(balance)
                balance = contract.total_cost - balance
            except ValueError:
                display_red_message(
                    "Le format n'est pas bon, ce champ attend un chiffre à virgule."
                    + "\nLa balance est définie à hauteur du coût du contrat."
                )
            if balance > contract.total_cost or balance < 0.0:
                display_red_message(
                    "Le prix payé ne peut pas être supérieur au coût"
                    + " du contrat ou inférieur à 0."
                    + "\nLa balance est définie à hauteur du coût du contrat."
                )
            elif balance <= contract.balance:
                display_red_message(
                    "Le prix payé ne peux pas être inférieur à la valeur précédente."
                )
            elif balance == contract.balance:
                display_red_message("Le prix payé n'à pas changé.")
        elif status == "Non signé":
            contract.status = StatusEnum.UNSIGNED
            contract.balance = contract.total_cost
        elif status == "Payé":
            contract.status = StatusEnum.PAID
            contract.balance = 0.0
        return contract

    def choice_menu(self, user_role):
        if user_role == "Manager":
            choice = self.menu.crud_menu("contrat")
        elif user_role == "Sales":
            choice = self.menu.global_menu(
                {
                    "t": "Voir tout les contrats",
                    "tf": "Voir les contrats filtrés par status",
                    "u": "Mettre à jour le contrat d'un de vos client",
                }
            )
        else:
            choice = self.menu.no_permission_menu("contrat")
        return choice
