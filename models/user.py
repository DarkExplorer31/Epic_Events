"""User model"""

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

ROLE = ["saleperson", "event manager", "support"]


class User(Base):
    def __init__(self, role, complete_name, email, phone_number):
        if role not in ROLE:
            raise ValueError("Invalid role")
        self.role = role
        self.complete_name = complete_name
        self.email = email
        self.phone_number = phone_number

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String, nullable=False)
    complete_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    creation_date = Column(Date, default=func.now(), nullable=False)
