"""User manager"""

from views.userview import UserView
from models.user_model import UserModel
from utils import Utils


class UserManager:
    def __init__(self, session, current_user):
        self.model = UserModel(session)
        self.view = UserView()
        self.current_user = current_user
        self.utils = Utils()

    def get_users(self):
        """This method is used to see all existing user"""
        all_users = self.model.get_all_users()
        self.view.display_users(all_users)

    def add_new_user(self, username):
        """Only for manager, this method add a new colaborator"""
        informations = self.view.add_new_user_view(username)
        if informations is None:
            return None
        new_user = self.model.create_user(informations)

        self.view.display_information(
            new_user,
            succes_message="Le nouvel utilisateur à été créer avec succès\n",
            error_message="Un problème est survenu, vérifier"
            + " que le numero de téléphone ou l'email n'est pas"
            + " déjà attribuer.\nL'utilisateur"
            + " n'a pas pu être créer.\n",
        )

    def update_user_information(self):
        """Only for manager, this method update colaborator's information"""
        self.get_users()
        email = self.view.find_user()
        if not email:
            return None
        user_to_update = self.model.search_user(loggin=email)
        if user_to_update:
            user_to_update = self.view.update_user_information_view(user_to_update)
            saved_user = self.model.update_user(user_to_update)
            self.view.display_information(
                saved_user,
                succes_message="L'utilisateur à été modifié avec succès\n",
                error_message="Un problème est survenu, vérifier"
                + " que le numero de téléphone n'est pas"
                + " déjà attribuer.\nL'utilisateur"
                + " n'a pas pu être mis à jour.\n",
            )
        else:
            self.utils.display_red_message("L'utilisateur recherché n'existe pas")

    def delete_user(self):
        """Only for manager, this method delete a colaborator in db"""
        self.get_users()
        email = self.view.find_user()
        if not email:
            return None
        user_to_delete = self.model.search_user(loggin=email)
        if user_to_delete:
            confirmation = self.view.confirm_choice(user_to_delete)
            if confirmation is True:
                delete_user = self.model.delete_user(user_to_delete)
                self.view.display_information(
                    delete_user,
                    succes_message="L'utilisateur à été supprimer avec succès",
                    error_message="Un problème est survenu, l'utilisateur"
                    + " n'a pas été supprimer.",
                )
            else:
                self.utils.display_red_message("L'utilisateur n'a pas été supprimer.")
        else:
            self.utils.display_red_message("L'utilisateur recherché n'existe pas")

    def run(self):
        username = self.current_user.complete_name
        role = self.current_user.role
        if role.value == "Manager":
            choice = self.view.user_menu()
            if not choice:
                return None
            elif choice == "t":
                self.get_users()
            elif choice == "a":
                self.add_new_user(username)
            elif choice == "u":
                self.update_user_information()
            elif choice == "d":
                self.delete_user()
        else:
            self.utils.display_red_message(
                "Vous n'avez pas accès au fonctionnalités de"
                + " cette partie du programme."
            )