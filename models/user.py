"""User model"""

import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Enum, Boolean
from db import Base


class RoleEnum(enum.Enum):
    SALESPERSON = "Saleperson"
    MANAGER = "Manager"
    SUPPORT = "Support"

    def __str__(self):
        return self.value


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    role = Column(Enum(RoleEnum), nullable=False)
    complete_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    password = Column(String)
    creation_date = Column(Date, default=datetime.now, nullable=False)
    first_using_password = Column(Boolean, default=True)

    def __init__(self, session):
        self.session = session

    def get_all_users(self):
        users_email = []
        users = self.session.query(User)
        for user in users:
            users_email.append(user.email)
        return users

    def search_user(self, loggin, password=None):
        if password:
            user = (
                self.session.query(User)
                .filter(
                    User.email == loggin,
                    User.password == password,
                )
                .first()
            )
        else:
            user = (
                self.session.query(User)
                .filter(
                    User.email == loggin,
                )
                .first()
            )
        if user:
            return user
        else:
            return None

    def add_user(self, new_user):
        self.session.add(new_user)
        self.session.commit()
        user_in_db = self.session.query(User).filter_by(id=new_user.email).first()
        if user_in_db:
            return True
        else:
            return False

    def update_user(self, user_to_update):
        """Update a User in Database.
        Only give to this method the user with informaton updated.
        Return a Boolean."""
        user_in_db = self.session.query(User).filter_by(id=user_to_update.id).first()
        if user_in_db:
            user_in_db.role = user_to_update.role
            user_in_db.complete_name = user_to_update.complete_name
            user_in_db.email = user_to_update.email
            user_in_db.phone_number = user_to_update.phone_number
            user_in_db.password = user_to_update.password
            user_in_db.creation_date = user_to_update.creation_date
            self.session.commit()
            return True
        else:
            return False

    def delete_user(self, user_to_delete):
        user_in_db = self.session.query(User).filter_by(id=user_to_delete.id).first()
        if user_in_db:
            self.session.delete(user_to_delete)
            self.session.commit()
            return True
        else:
            return False
