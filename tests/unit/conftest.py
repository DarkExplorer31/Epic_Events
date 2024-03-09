"""Configuration for tests"""

import pytest
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(project_root)

from db import Base


class DataBaseManager:
    def __init__(self, db_uri):
        self.db_uri = db_uri
        self.session = self.create_db_session()

    def create_db_session(self):
        engine = create_engine(self.db_uri)
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session

    def drop_all_tables(self):
        engine = create_engine(self.db_uri)
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def db_manager():
    db_uri = "sqlite:///test_database.db"
    manager = DataBaseManager(db_uri)
    yield manager
    manager.drop_all_tables()


@pytest.fixture(scope="module")
def session(db_manager):
    return db_manager.session
