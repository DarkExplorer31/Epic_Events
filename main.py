"""Define main"""

from db import DataBase
from controllers.authenticationmanager import AuthenticationController
from controllers.usermanager import UserManager
from controllers.clientmanager import ClientManager
from controllers.contractmanager import ContractManager
from controllers.eventmanager import EventManager


def call_controller_by_choice(choice, session, user):
    user_manager = UserManager(session, user)
    client_manager = ClientManager(session, user)
    contract_manager = ContractManager(session, user)
    event_manager = EventManager(session, user)
    if choice == "u":
        user_manager.menu()
    elif choice == "c":
        contract_manager.menu()
    elif choice == "e":
        event_manager.menu()
    elif choice == "cl":
        client_manager.menu()


def main():
    db_instance = DataBase()
    db_session = db_instance.create_db_session()
    if db_session:
        authentication_controller = AuthenticationController(db_session)
        authenticate_user = authentication_controller.authenticate()
        if not authenticate_user:
            return None
        choice = ""
        while choice != "q":
            choice = authentication_controller.main_menu(user=authenticate_user)
            call_controller_by_choice(choice, db_session, authenticate_user)
        db_session.close()


if __name__ == "__main__":
    main()
