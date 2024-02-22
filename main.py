"""Define main"""

from db import DataBase
from controllers.authenticationmanager import AuthenticationController
from controllers.crmmanager import CRMManager


def main():
    db_instance = DataBase()
    db_session = db_instance.create_db_session()
    if db_session:
        authentication_controller = AuthenticationController(db_session)
        authenticate_user = authentication_controller.authenticate()
        if not authenticate_user:
            return None
        choice = ""
        crm = CRMManager(db_session, authenticate_user)
        while choice != "q":
            choice = authentication_controller.main_menu(user=authenticate_user)
            crm.run(choice)
        db_session.close()


if __name__ == "__main__":
    main()
