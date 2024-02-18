"""Define main"""

from db import DataBase
from controllers.authenticationmanager import AuthenticationController
from controllers.usermanager import UserManager


def main():
    db_instance = DataBase()
    db_session = db_instance.create_db_session()
    if db_session:
        authentication_controller = AuthenticationController(db_session)
        authenticate_user = authentication_controller.authenticate()
        if not authenticate_user:
            return None
        choice = authentication_controller.main_menu(user=authenticate_user)
        while choice != "q":
            choice = authentication_controller.main_menu(user=authenticate_user)
            if choice == "u":
                user_controller = UserManager()
                user_controller.run()
            elif choice == "c":
                pass
            elif choice == "e":
                pass
            elif choice == "cl":
                pass


if __name__ == "__main__":
    main()
