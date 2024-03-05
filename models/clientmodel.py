"""Client model"""

import datetime
from sqlalchemy.exc import IntegrityError

from .db_models import Client


class ClientModel:
    def __init__(self, session):
        self.session = session

    def create(self, user_id, complete_name, email, phone_number, company_name):
        try:
            new_client = Client(
                user_id=user_id,
                complete_name=complete_name,
                email=email,
                phone_number=phone_number,
                company_name=company_name,
            )
            self.session.add(new_client)
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
            return False

    def get_all(self):
        return self.session.query(Client).all()

    def get_all_by_user_responsibility(self, user_id):
        return self.session.query(Client).filter(Client.user_id == user_id).all()

    def search(self, email):
        return self.session.query(Client).filter(Client.email == email).first()

    def update(self, client_to_update):
        try:
            client_in_db = (
                self.session.query(Client).filter_by(id=client_to_update.id).first()
            )
            if not client_in_db:
                return False
            client_in_db.complete_name = client_to_update.complete_name
            client_in_db.email = client_to_update.email
            client_in_db.phone_number = client_to_update.phone_number
            client_in_db.company_name = client_to_update.company_name
            client_in_db.updating_date = datetime.datetime.now()
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
            return False

    def delete(self, client_to_delete):
        client_in_db = (
            self.session.query(Client).filter_by(email=client_to_delete.email).first()
        )
        if not client_in_db:
            return False
        self.session.delete(client_to_delete)
        self.session.commit()
        return True
