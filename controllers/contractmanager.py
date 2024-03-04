"""Contract manager"""

from models.contractmodel import ContractModel
from models.clientmodel import ClientModel
from views.contractview import ContractView


class ContractManager:

    def __init__(self, session, user_authenticate):
        self.model = ContractModel(session)
        self.client_model = ClientModel(session)
        self.view = ContractView()
        self.role = user_authenticate.role.value
        self.user_id = user_authenticate.id

    # Obtaining methods
    def get_all_contracts(self):
        all_contracts = self.model.get_all()
        self.view.display_contracts(all_contracts)

    def get_all_clients_under_responsibility(self):
        if self.role == "Manager":
            all_clients = self.client_model.get_all()
        else:
            all_clients = self.client_model.get_all_by_user_responsibility(self.user_id)
        self.view.display_clients_under_responsibility(all_clients)

    def get_all_contracts_by_filter(self):
        status = self.view.ask_status()
        if not status:
            return None
        all_contracts = self.model.get_all_by_status(status)
        self.view.display_contracts(all_contracts)

    # Searching methods
    def select_contract(self):
        self.get_all_contracts()
        search_id = self.view.search_contract()
        contract = self.model.search(id=search_id)
        if not contract:
            self.view.display_unfound_contract()
        return contract

    def select_client_under_responsibility(self):
        """Responsibility changes according to user role.
        If the user is a Manager, all clients are under his responsibility."""
        self.get_all_clients_under_responsibility()
        search_email = self.view.search_client_under_responsibility()
        client = self.client_model.search(email=search_email)
        if client and self.role != "Manager" and client.user_id != self.user_id:
            self.view.display_client_is_not_under_responsibility()
        elif not client:
            self.view.display_unfound_client()
        return client

    # Create method
    def create_new_contract(self):
        concerned_client = self.select_client_under_responsibility()
        if not concerned_client:
            return None
        data = self.view.get_new_contract_information()
        if not data:
            return None
        creation = self.model.create(
            user_id=self.user_id,
            client_id=concerned_client.id,
            total_cost=data["total_cost"],
            balance=data["balance"],
            status=data["status"],
        )
        if creation:
            self.view.display_created()
        else:
            self.view.display_not_created()

    # Update method
    def update_contract(self):
        contract_to_update = self.select_contract()
        if not contract_to_update:
            return None
        if self.role != "Manager" and contract_to_update.user_id != self.user_id:
            self.view.display_contract_is_not_under_responsibility()
            return None
        updated_contract = self.view.get_update_contract_informations(
            contract_to_update
        )
        update = self.model.update(updated_contract)
        if update:
            self.view.display_contract_is_update()
        else:
            self.view.display_contract_is_not_update()

    # Delete method
    def delete_contract(self):
        contract_to_delete = self.select_contract()
        if not contract_to_delete:
            return None
        confirmation = self.view.delete_confirmation(contract_to_delete.id)
        if not confirmation:
            return None
        deletion = self.model.delete(contract_to_delete.id)
        if deletion:
            self.view.display_contract_is_delete()
        else:
            self.view.display_contract_is_not_delete()

    # Main method
    def menu(self):
        choice = self.view.choice_menu(self.role)
        if not choice:
            return None
        elif choice == "t":
            self.get_all_contracts()
        elif choice == "a" and self.role in ["Sales", "Manager"]:
            self.create_new_contract()
        elif choice == "u" and self.role in ["Sales", "Manager"]:
            self.update_contract()
        elif choice == "d" and self.role in ["Sales", "Manager"]:
            self.delete_contract()
        else:
            self.view.display_not_authorized()
