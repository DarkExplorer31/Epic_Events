
"""Client model"""

import datetime
from sqlalchemy.exc import IntegrityError

from .db_models import Client


class ClientModel:
    def __init__(self, session):
        self.session = session

    def create_client(self, current_user, informations):
        try:
            new_client = Client(
                user_id=current_user,
                complete_name=informations[0],
                email=informations[1],
                phone_number=informations[2],
                company_name=informations[3],
            )
            self.session.add(new_client)
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
            return False

    def get_all_clients(self):
        clients = self.session.query(Client)
        return clients

    def search_client(self, email):
        if email:
            client = (
                self.session.query(Client)
                .filter(
                    Client.email == email).first())
            if client:
                return client
            else:
                return None
        else:
            return None

    def update_client(self, client_to_update):
        """Update a Client in Database"""
        client_in_db = self.session.query(Client).filter_by(id=client_to_update.id).first()
        if client_in_db:
            try:
                client_in_db.complete_name = client_to_update.complete_name
                client_in_db.email = client_to_update.email
                client_in_db.phone_number = client_to_update.phone_number
                client_in_db.company_name = client_to_update.company_name
                client_in_db.updating_date = datetime.now
                self.session.commit()
                return True
            except IntegrityError:
                self.session.rollback()
                return False
        else:
            return False

    def delete_client(self, client_to_delete):
        client_in_db = self.session.query(Client).filter_by(id=client_to_delete.id).first()
        if client_in_db:
            self.session.delete(client_to_delete)
            self.session.commit()
            return True
        else:
            return False