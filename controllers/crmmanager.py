"""CRM Manager"""

from models.usermodel import UserModel
from models.clientmodel import ClientModel
from models.contractmodel import ContractModel
from models.eventmodel import EventModel
from views.userview import UserView
from views.clientview import ClientView
from views.contractview import ContractView
from views.eventview import EventView
from utils import display_red_message, Menu


class CRMManager:

    def __init__(self, session, user_authenticate):
        self.current_user = user_authenticate
        self.role = self.current_user.role
        self.concerned_object = ""
        self.menu = Menu()
        # models
        self.user_model = UserModel(session)
        self.client_model = ClientModel(session)
        self.contract_model = ContractModel(session)
        self.event_model = EventModel(session)
        # views
        self.user_view = UserView()
        self.client_view = ClientView()
        self.contract_view = ContractView()
        self.event_view = EventView()

    def get_all_objects(self):
        """Get all objects in database"""
        if self.concerned_object == "user":
            all_users = self.user_model.get_all_users()
            self.user_view.display_users(all_users)
        elif self.concerned_object == "client":
            all_clients = self.client_model.get_all_clients()
            self.client_view.display_all_clients(all_clients)
        elif self.concerned_object == "contract":
            all_contracts = self.contract_model.get_all_contracts()
            self.contract_view.display_all_contracts(all_contracts)
        elif self.concerned_object == "event":
            all_events = self.event_model.get_all_events()
            self.display_all_events(all_events)

    # Add object part
    def get_informations_for_add_new_object(self):
        """Take all informations to add an object on database"""
        if self.concerned_object == "user":
            informations = self.user_view.add_new_user_view(
                self.current_user.complete_name
            )
        elif self.concerned_object == "client":
            informations = self.client_view.add_new_client_view()
        elif self.concerned_object == "contract":
            all_client_table = self.client_model.is_empty_table()
            if all_client_table:
                display_red_message(
                    "Un problème est survenu.\nLe contrat n'a pas pu "
                    + "être créer car vous n'avez pas encore de client"
                    + " dans la base de donnée.\n"
                )
                return None
            informations = self.contract_view.add_new_contract_view()
        elif self.concerned_object == "event":
            informations = self.event_view.add_new_event_view()
        return informations

    def add_new_object(self):
        informations = self.get_informations_for_add_new_object()
        if informations is None:
            return None
        elif self.concerned_object == "user":
            new_user = self.user_model.create_user(informations)
            self.menu.display_result_information(
                new_user,
                succes_message="Le nouvel utilisateur à été créer avec succès\n",
                error_message="Un problème est survenu, vérifier"
                + " que le numero de téléphone ou l'email n'est pas"
                + " déjà attribuer.\nL'utilisateur"
                + " n'a pas pu être créer.\n",
            )
        elif self.concerned_object == "client":
            new_client = self.client_model.create_client(
                self.current_user, informations
            )
            self.menu.display_result_information(
                new_client,
                succes_message="Le nouveau client à été créer avec succès\n",
                error_message="Un problème est survenu, vérifier"
                + " que le numero de téléphone ou l'email n'est pas"
                + " déjà attribuer.\nLe client"
                + " n'a pas pu être créer.\n",
            )
        elif self.concerned_object == "contract":
            client_email = self.client_view.find_client()
            if not client_email:
                return None
            selected_client = self.client_model.get_a_client(client_email)
            if selected_client:
                new_contract = self.contract_model.create_contract(
                    self.current_user, selected_client, informations
                )
                self.menu.display_result_information(
                    new_contract,
                    succes_message="Le nouveau contrat à été créer avec succès\n",
                    error_message="Un problème est survenu: le client"
                    + " n'existe pas.\nLe contrat"
                    + " n'a pas pu être créer.\n",
                )
            else:
                display_red_message(
                    "Un problème est survenu.\nLe contrat n'a pas pu être créer.\n"
                )
        elif self.concerned_object == "event":
            selected_contract = self.contract_view.find_contract()
            if selected_contract:
                new_event = self.event_model.create_event(
                    selected_contract, informations
                )
                self.menu.display_result_information(
                    new_event,
                    succes_message="L'évènement à été créer avec succès\n",
                    error_message="Un problème est survenu.\nL'évènement"
                    + " n'a pas pu être créer.\n",
                )
            else:
                display_red_message(
                    "Un problème est survenu.\nL'évènement n'a pas pu être créer.\n"
                )

    # Update and Delete object part
    def get_object(self):
        self.get_all_objects()
        if self.concerned_object == "user":
            email = self.user_view.find_user()
            if not email:
                return None
            user_to_update = self.user_model.search_user(loggin=email)
            if user_to_update:
                return user_to_update
            else:
                display_red_message("L'utilisateur recherché n'existe pas")
                return None
        elif self.concerned_object == "client":
            email = self.client_view.find_client()
            if not email:
                return None
            client_to_update = self.client_model.search_client(email=email)
            if client_to_update:
                if client_to_update.user_id == self.current_user.id:
                    return client_to_update
                else:
                    display_red_message("Vous n'êtes pas responsable de ce client")
                    return None
            else:
                display_red_message("Le client recherché n'existe pas")
                return None
        elif self.concerned_object == "contract":
            id = self.contract_view.find_contract()
            if not id:
                return None
            contract_to_update = self.contract_model.search_contract(id)
            if contract_to_update and self.current_user.role.value == "Manager":
                return contract_to_update
            else:
                if contract_to_update.user_id == self.current_user.id:
                    return contract_to_update
                else:
                    display_red_message("Vous n'êtes pas responsable de ce client")
                    return None
        elif self.concerned_object == "event":
            id = self.event_view.find_event()
            if not id:
                return None
            event_to_update = self.event_model.search_event(id)
            if event_to_update:
                return event_to_update

    def update_object(self):
        object_to_update = self.get_object()
        if not object_to_update:
            return None
        if self.concerned_object == "user":
            update_user = self.user_view.update_user_informations_view(object_to_update)
            if not update_user:
                return None
            saved_user = self.user_model.update_user(update_user)
            self.menu.display_result_information(
                saved_user,
                succes_message="L'utilisateur à été modifié avec succès\n",
                error_message="Un problème est survenu, vérifier"
                + " que le numero de téléphone n'est pas"
                + " déjà attribuer.\nL'utilisateur"
                + " n'a pas pu être mis à jour.\n",
            )
        elif self.concerned_object == "client":
            update_client = self.client_view.update_client_informations_view(
                object_to_update
            )
            if not update_client:
                return None
            saved_client = self.client_model.update_client(update_client)
            self.menu.display_result_information(
                saved_client,
                succes_message="Le client à été modifié avec succès\n",
                error_message="Un problème est survenu, vérifier"
                + " que le numero de téléphone n'est pas"
                + " déjà attribuer.\nLe client"
                + " n'a pas pu être mis à jour.\n",
            )
        elif self.concerned_object == "contract":
            client = self.client_model.search_client(id=object_to_update.client_id)
            update_contract = self.contract_view.update_contract_informations_view(
                client, object_to_update
            )
            if not update_contract:
                return None
            saved_contract = self.contract_model.update_contract(update_contract)
            self.menu.display_result_information(
                saved_contract,
                succes_message="Le contrat à été modifié avec succès\n",
                error_message="Un problème est survenu.\nLe contrat"
                + " n'a pas pu être mis à jour.\n",
            )
        elif self.concerned_object == "event":
            if self.current_user.role.value == "Manager":
                update_event = self.event_view.update_support_assignated_view(
                    object_to_update
                )
            elif self.current_user.role.value == "Support":
                update_event = self.event_view.update_event_informations_view(
                    object_to_update
                )
            if not update_event:
                return None
            saved_event = self.event_model.update_contract(update_event)
            self.menu.display_result_information(
                saved_event,
                succes_message="L'évènement à été modifié avec succès\n",
                error_message="Un problème est survenu.\nL'évènement"
                + " n'a pas pu être mis à jour.\n",
            )

    def delete_object(self):
        object_to_delete = self.get_object()
        if not object_to_delete:
            return None
        if self.concerned_object == "user":
            confirmation = self.menu.confirm_choice(object_to_delete.complete_name)
            if confirmation is True:
                delete_user = self.user_model.delete_user(object_to_delete)
                self.menu.display_result_information(
                    delete_user,
                    succes_message="L'utilisateur à été supprimer avec succès",
                    error_message="Un problème est survenu, l'utilisateur"
                    + " n'a pas été supprimer.",
                )
            else:
                display_red_message("L'utilisateur n'a pas été supprimer.")
        elif self.concerned_object == "client":
            confirmation = self.menu.confirm_choice(object_to_delete.complete_name)
            if confirmation is True:
                delete_client = self.client_model.delete_client(object_to_delete)
                self.menu.display_result_information(
                    delete_client,
                    succes_message="Le client à été supprimer avec succès",
                    error_message="Un problème est survenu, le client"
                    + " n'a pas été supprimer.",
                )
            else:
                display_red_message("Le client n'a pas été supprimer.")
        elif self.concerned_object == "contract":
            confirmation = self.menu.confirm_choice(object_to_delete.id)
            if confirmation is True:
                delete_contract = self.contract_model.delete_contract(object_to_delete)
                self.menu.display_result_information(
                    delete_contract,
                    succes_message="Le contrat à été supprimer avec succès",
                    error_message="Un problème est survenu, le contrat"
                    + " n'a pas été supprimer.",
                )
            else:
                display_red_message("Le contrat n'a pas été supprimer.")
        elif self.concerned_object == "event":
            confirmation = self.menu.confirm_choice(object_to_delete.id)
            if confirmation is True:
                delete_contract = self.event_model.delete_event(object_to_delete)
                self.menu.display_result_information(
                    delete_contract,
                    succes_message="L'évènement à été supprimer avec succès",
                    error_message="Un problème est survenu, L'évènement"
                    + " n'a pas été supprimer.",
                )
            else:
                display_red_message("L'évènement n'a pas été supprimer.")

    def menu_by_choice(
        self, selected, designation, role_without_permission, role_with_all_permission
    ):
        if selected not in ["user", "client", "contract", "event"]:
            raise ValueError
        self.concerned_object = selected
        if self.role.value in role_without_permission:
            choice = self.menu.no_permission_menu()
            if not choice:
                return None
            elif choice == "t":
                self.get_all_objects()
        elif self.role.value in role_with_all_permission:
            choice = self.menu.crud_menu(designation)
            if not choice:
                return None
            elif choice == "t":
                self.get_all_objects()
            elif choice == "a":
                self.add_new_object()
            elif choice == "u":
                self.update_object()
            elif choice == "d":
                self.delete_object()

    def run(self, choice):
        if choice == "u":
            role_with_all_permission = ["Manager"]
            role_without_all_permission = ["Sales", "Support"]
            self.menu_by_choice(
                "user",
                "utilisateur",
                role_without_all_permission,
                role_with_all_permission,
            )
        elif choice == "c":
            role_with_all_permission = ["Manager", "Sales"]
            role_without_all_permission = ["Support"]
            self.menu_by_choice(
                "contract",
                "contrat",
                role_without_all_permission,
                role_with_all_permission,
            )
        elif choice == "e":
            role_with_all_permission = ["Manager", "Sales", "Support"]
            role_without_all_permission = []
            self.menu_by_choice(
                "event",
                "évènement",
                role_without_all_permission,
                role_with_all_permission,
            )
        elif choice == "cl":
            role_with_all_permission = ["Sales"]
            role_without_all_permission = ["Support", "Manager"]
            self.menu_by_choice(
                "client",
                "client",
                role_without_all_permission,
                role_with_all_permission,
            )
