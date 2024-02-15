"""Define main"""

from db import DataBase
from controllers.authenticationmanager import AuthenticationController


def main():
    db_instance = DataBase()
    db_session = db_instance.create_db_session()
    if db_session:
        auth_controller = AuthenticationController(db_session)
        auth_controller.main_menu()


if __name__ == "__main__":
    main()
