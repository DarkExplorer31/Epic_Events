"""User manager"""

from models.usermodel import UserModel
from views.userview import UserView


class UserManager:

    def __init__(self, session, user_authenticate):
        self.model = UserModel(session)
        self.view = UserView()
        self.role = user_authenticate.role.value

    # Obtaining methods
    def get_all_users(self):
        all_users = self.model.get_all()
        self.view.display_users(all_users)

    def get_all_support(self):
        all_support_users = self.model.get_all_support_user()
        self.view.display_users(all_support_users)

    # Create method
    def create_new_user(self):
        data = self.view.get_new_user_information()
        if not data:
            return None
        creation = self.model.create(
            role=data["role"],
            complete_name=data["complete_name"],
            email=data["email"],
            phone_number=data["phone_number"],
            password=data["password"],
        )
        if creation:
            self.view.display_created()
        else:
            self.view.display_not_created()

    # Searching method
    def select_user(self):
        self.get_all_users()
        search_email = self.view.search_user()
        user = self.model.search(loggin=search_email)
        if not user:
            self.view.display_unfound_user()
        return user

    # Update method
    def update_user(self):
        user_to_update = self.select_user()
        if not user_to_update:
            return None
        updated_user = self.view.get_update_user_informations(user_to_update)
        update = self.model.update(updated_user)
        if update:
            self.view.display_user_is_update()
        else:
            self.view.display_user_is_not_update()

    # Delete method
    def delete_user(self):
        user_to_delete = self.select_user()
        if not user_to_delete:
            return None
        confirmation = self.view.delete_confirmation(user_to_delete.email)
        if not confirmation:
            return None
        deletion = self.model.delete(user_to_delete.id)
        if deletion:
            self.view.display_user_is_delete()
        else:
            self.view.display_user_is_not_delete()

    # Main method
    def menu(self):
        if self.role != "Manager":
            self.view.display_user_is_not_authorized()
        choice = self.view.choice_menu()
        if not choice:
            return None
        elif choice == "t":
            self.get_all_users()
        elif choice == "a":
            self.create_new_user()
        elif choice == "u":
            self.update_user()
        elif choice == "d":
            self.delete_user()
