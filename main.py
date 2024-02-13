"""Define main"""

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from models.user import Base
from controllers.authenticationcontroller import AuthenticationController


def manage_db():
    engine = create_engine("sqlite:///epic_event.db")
    try:
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session
    except SQLAlchemyError as e:
        print("Erreur lors de la création de la base de données :", e)


def main():
    # created user in db with email = bc@gmail.com and password = lol
    db_session = manage_db()
    auth_controller = AuthenticationController(db_session)
    auth_controller.authenticate()


if __name__ == "__main__":
    main()
