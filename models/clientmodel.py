"""Client model"""

from sqlalchemy.exc import IntegrityError

from .db_models import Client


class ClientModel:
    def __init__(self, session):
        self.session = session

    def create_client(self, informations):
        try:
            new_client = Client(
                user_id=informations[0],
                complete_name=informations[1],
                email=informations[2],
                phone_number=informations[3],
                company_name=informations[4],
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
