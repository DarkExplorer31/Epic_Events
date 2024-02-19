"""Define User model for DataBase"""

import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Enum, Boolean
from db import Base


class RoleEnum(enum.Enum):
    SALES = "Sales"
    MANAGER = "Manager"
    SUPPORT = "Support"

    def __str__(self):
        return self.value


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    role = Column(Enum(RoleEnum), nullable=False)
    complete_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    password = Column(String)
    creation_date = Column(Date, default=datetime.now, nullable=False)
    first_using_password = Column(Boolean, default=True)

    def __str__(self):
        return self.email
