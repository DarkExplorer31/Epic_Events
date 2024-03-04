"""User model"""

import hashlib
from sqlalchemy.exc import IntegrityError

from .db_models import User


class UserModel:
    def __init__(self, session):
        self.session = session

    def create(self, role, complete_name, email, phone_number, password):
        try:
            password = hashlib.sha256(password.encode()).hexdigest()
            role = role.upper()
            new_user = User(
                role=role,
                complete_name=complete_name,
                email=email,
                phone_number=phone_number,
                password=password,
            )
            self.session.add(new_user)
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
            return False

    def get_all(self):
        return self.session.query(User).all()

    def get_all_support_user(self):
        return self.session.query(User).filter_by(role="SUPPORT").all()

    def search(self, loggin, password=None):
        if password:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            return (
                self.session.query(User)
                .filter(
                    User.email == loggin,
                    User.password == hashed_password,
                )
                .first()
            )
        else:
            return (
                self.session.query(User)
                .filter(
                    User.email == loggin,
                )
                .first()
            )

    def change_password(self, user_id, new_password):
        user_in_db = self.session.query(User).filter_by(id=user_id).first()
        if user_in_db:
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            user_in_db.password = hashed_password
            user_in_db.first_using_password = False
            self.session.commit()
            return True
        else:
            return False

    def update(self, user_to_update):
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

    def delete(self, user_id):
        user_in_db = self.session.query(User).filter_by(id=user_id).first()
        if user_in_db:
            self.session.delete(user_in_db)
            self.session.commit()
            return True
        else:
            return False
