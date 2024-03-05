"""Client manager"""

from models.clientmodel import ClientModel
from views.clientview import ClientView


class ClientManager:

    def __init__(self, session, user_authenticate):
        self.model = ClientModel(session)
        self.view = ClientView()
        self.role = user_authenticate.role.value
        self.user_id = user_authenticate.id

    # Obtaining methods
    def get_all_clients(self):
        all_clients = self.model.get_all()
        self.view.display_clients(all_clients)

    # Create method
    def create_new_client(self):
        data = self.view.get_new_client_information()
        if not data:
            return None
        creation = self.model.create(
            user_id=self.user_id,
            complete_name=data["complete_name"],
            email=data["email"],
            phone_number=data["phone_number"],
            company_name=data["company_name"],
        )
        if creation:
            self.view.display_created()
        else:
            self.view.display_not_created()

    # Searching method
    def select_client(self):
        self.get_all_clients()
        search_email = self.view.search_client()
        client = self.model.search(email=search_email)
        if not client:
            self.view.display_unfound_client()
        return client

    # Update method
    def update_client(self):
        client_to_update = self.select_client()
        if not client_to_update:
            return None
        if client_to_update.user_id != self.user_id:
            self.view.display_client_is_not_under_responsibility()
            return None
        updated_client = self.view.get_update_client_informations(client_to_update)
        update = self.model.update(updated_client)
        if update:
            self.view.display_client_is_update()
        else:
            self.view.display_client_is_not_update()

    # Delete method
    def delete_client(self):
        client_to_delete = self.select_client()
        if not client_to_delete:
            return None
        if client_to_delete.user_id != self.user_id:
            self.view.display_client_is_not_under_responsibility()
            return None
        deletion = self.model.delete(client_to_delete)
        if deletion:
            self.view.display_client_is_delete()
        else:
            self.view.display_client_is_not_delete()

    # Main method
    def menu(self):
        choice = self.view.choice_menu(self.role)
        if not choice:
            return None
        elif choice == "t":
            self.get_all_clients()
        elif choice == "a" and self.role == "Sales":
            self.create_new_client()
        elif choice == "u" and self.role == "Sales":
            self.update_client()
        elif choice == "d" and self.role == "Sales":
            self.delete_client()
        else:
            self.view.display_not_authorized()
