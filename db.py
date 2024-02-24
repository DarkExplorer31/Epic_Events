"""DataBase manager"""

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class DataBase:

    def create_db_session(self):
        engine = create_engine("sqlite:///epic_event.db")
        try:
            Base.metadata.create_all(bind=engine)
            Session = sessionmaker(bind=engine)
            session = Session()
            return session
        except SQLAlchemyError as e:
            print("Erreur lors de la création de la base de données :", e)
