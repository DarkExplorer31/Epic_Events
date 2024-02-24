"""CRM Manager"""

from models.usermodel import UserModel
from models.clientmodel import ClientModel
from views.userview import UserView
from views.clientview import ClientView
from utils import display_red_message


class CRMManager:

    def __init__(self, session, user_authenticate):
        # define
        self.current_user = user_authenticate
        # models
        self.user_model = UserModel(session)
        self.client_model = ClientModel(session)
        # views
        self.user_view = UserView()
        self.client_view = ClientView()

    def get_all_objects(self, concerned_object):
        """Get all objects in database"""
        if concerned_object == "user":
            all_users = self.user_model.get_all_users()
            self.user_view.display_users(all_users)
        elif concerned_object == "client":
            all_clients = self.client_model.get_all_clients()
            self.client_view.display_all_clients(all_clients)

    # Add object part
    def get_informations_for_add_new_object(self, concerned_object):
        """Take all informations to add an object on database"""
        if concerned_object == "user":
            informations = self.view.add_new_user_view(self.curent_user.complete_name)
        elif concerned_object == "client":
            informations = self.view.add_new_client_view()
        else:
            return informations

    def add_new_object(self, concerned_object):
        informations = self.get_informations_for_add_new_object(concerned_object)
        if informations is None:
            return None
        if concerned_object == "user":
            new_user = self.model.create_user(informations)
            self.menu.display_result_information(
                new_user,
                succes_message="Le nouvel utilisateur à été créer avec succès\n",
                error_message="Un problème est survenu, vérifier"
                + " que le numero de téléphone ou l'email n'est pas"
                + " déjà attribuer.\nL'utilisateur"
                + " n'a pas pu être créer.\n",
            )
        elif concerned_object == "client":
            new_client = self.client_model.create_client(self.current_user,informations)
            self.menu.display_result_information(
                new_client,
                succes_message="Le nouveau client à été créer avec succès\n",
                error_message="Un problème est survenu, vérifier"
                + " que le numero de téléphone ou l'email n'est pas"
                + " déjà attribuer.\nLe client"
                + " n'a pas pu être créer.\n",
            )
        elif concerned_object == "contract":
            pass

    # Update and Delete object part
    def get_object(self, concerned_object):
        if concerned_object == "user":
            self.get_all_objects(concerned_object)
            email = self.user_view.find_user()
            if not email:
                return None
            user_to_update = self.user_model.search_user(loggin=email)
            if user_to_update:
                return user_to_update
            else:
                display_red_message("L'utilisateur recherché n'existe pas")
                return None
        elif concerned_object == "client":
            pass

    def update_object(self, concerned_object):
        object_to_update = self.get_object(concerned_object)
        if not object_to_update:
            return None
        if concerned_object == "user":
            saved_user = self.user_model.update_user(object_to_update)
            self.menu.display_result_information(
                saved_user,
                succes_message="L'utilisateur à été modifié avec succès\n",
                error_message="Un problème est survenu, vérifier"
                + " que le numero de téléphone n'est pas"
                + " déjà attribuer.\nL'utilisateur"
                + " n'a pas pu être mis à jour.\n",
            )
        elif concerned_object == "client":
            pass

    def delete_object(self, concerned_object):
        object_to_delete = self.get_object(concerned_object)
        if not object_to_delete:
            return None
        if concerned_object == "user":
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
        elif concerned_object == "client":
            pass

    def user_menu(self):
        current_menu = "user"
        role = self.current_user.role
        if role.value == "Manager":
            choice = self.user_view.user_menu()
            if not choice:
                return None
            elif choice == "t":
                self.get_object(current_menu)
            elif choice == "a":
                self.add_new_object(current_menu)
            elif choice == "u":
                self.update_object(current_menu)
            elif choice == "d":
                self.delete_object(current_menu)
        else:
            display_red_message(
                "Vous n'avez pas accès au fonctionnalités de"
                + " cette partie du programme."
            )

    def run(self, choice):
        if choice == "u":
            self.user_menu()
        elif choice == "c":
            pass
        elif choice == "e":
            pass
        elif choice == "cl":
            pass
