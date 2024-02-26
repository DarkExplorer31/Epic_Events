"""Contract view"""

from models.db_models import StatusEnum
from utils import Menu, display_green_message, display_red_message


class ContractView:
    STATUS = ["Non signé", "Pas payer", "Payer"]

    def __init__(self):
        self.menu = Menu()

    def display_all_contracts(self, all_contracts):
        if all_contracts:
            display_green_message("Voici la liste des contrats actuels:\n")
            for contrat in all_contracts:
                print(contrat)
        else:
            display_red_message("Votre liste de contrat actuel est vide.\n")

    def display_status(self):
        print("Les status qui peuvent être entrés: ")
        for choice_status in self.STATUS:
            print(f"-{choice_status}")
        print("\n")

    def add_new_contract_view(self):
        print(f"Bienvenue dans la création d'un nouveau contrat\n")
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
                not_conform_message="Le status doit être 'Non signé', 'Pas payer' ou 'Payer'",
            )
            if not status:
                return None
            if status == "Non Payer":
                status = StatusEnum.UNPAID
                balance = self.menu.information_menu(
                    asking_sentence="Veuillez remplir le coût déjà payer par le client"
                )
                if not balance:
                    return None
                try:
                    balance = float(balance)
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
                        + "\nLa balance est définie à hauteur du coût du contrat."
                    )
                    balance = total_cost
            elif status == "Non signé":
                status = StatusEnum.UNSIGNED
                balance = total_cost
            elif status == "Payer":
                status = StatusEnum.PAID
                balance = 0.01
            return [total_cost, balance, status]

    def find_contract(self):
        print(f"Bienvenue dans la fonction de recherche d'un contrat")
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

    def update_contract_informations_view(self, client, contract):
        print(
            "\n"
            + f"Vous voulez mettre à jour les informations de {client.company_name}."
            + f"Le contrat à été créer le: {contract.creation_date}"
            + "\n"
            + f"le montant total est de : {contract.total_cost}"
            + "\n"
            + f"et le status est: {contract.status}"
        )
        self.display_status()
        status = self.menu.information_menu(
            asking_sentence="Veuillez remplir le status actuel du contrat",
            possible_response=self.STATUS,
            not_conform_message="Le status doit être 'Non signé', 'Pas payer' ou 'Payer'",
        )
        if not status:
            return None
        elif status == contract.status:
            display_red_message("Le status n'a pas changé")
        elif status == "Non Payer":
            contract.status = StatusEnum.UNPAID
            balance = self.menu.information_menu(
                asking_sentence="Veuillez remplir le coût déjà payer par le client"
            )
            if not balance:
                display_red_message("La balance n'a pas changée")
                return None
            try:
                balance = float(balance)
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
        elif status == "Payer":
            contract.status = StatusEnum.PAID
            contract.balance = 0.01
        return contract
