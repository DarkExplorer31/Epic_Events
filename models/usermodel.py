"""User model"""

import hashlib
from sqlalchemy.exc import IntegrityError

from .db_models import User


class UserModel:
    def __init__(self, session):
        self.session = session

    def create_user(self, user_info):
        try:
            user_info[4] = hashlib.sha256(user_info[4].encode()).hexdigest()
            user_info[0] = user_info[0].upper()
            new_user = User(
                role=user_info[0],
                complete_name=user_info[1],
                email=user_info[2],
                phone_number=user_info[3],
                password=user_info[4],
            )
            self.session.add(new_user)
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
            return False

    def get_all_users(self):
        users_email = []
        users = self.session.query(User)
        for user in users:
            users_email.append(user)
        return users

    def search_user(self, loggin, password=None):
        if password:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            user = (
                self.session.query(User)
                .filter(
                    User.email == loggin,
                    User.password == hashed_password,
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

    def change_password(self, user_id, new_password):
        """Change the password of a user."""
        user_in_db = self.session.query(User).filter_by(id=user_id).first()
        if user_in_db:
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            user_in_db.password = hashed_password
            user_in_db.first_using_password = False
            self.session.commit()
            return True
        else:
            return False

    def update_user(self, user_to_update):
        """Update a User in Database.
        Only give to this method the user with informaton updated.
        Return a Boolean."""
        try:
            user_in_db = (
                self.session.query(User).filter_by(id=user_to_update.id).first()
            )
            if not user_in_db:
                return False
            user_in_db.role = user_to_update.role
            user_in_db.complete_name = user_to_update.complete_name
            user_in_db.email = user_to_update.email
            user_in_db.phone_number = user_to_update.phone_number
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
            return False

    def delete_user(self, user_to_delete):
        user_in_db = self.session.query(User).filter_by(id=user_to_delete.id).first()
        if user_in_db:
            self.session.delete(user_to_delete)
            self.session.commit()
            return True
        else:
            return False
