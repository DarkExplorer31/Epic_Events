"""Contract model"""

import datetime
from sqlalchemy.exc import IntegrityError

from .db_models import Contract, Client


class ContractModel:
    def __init__(self, session):
        self.session = session

    def create(self, user_id, client_id, total_cost, balance, status):
        try:
            new_contract = Contract(
                user_id=user_id,
                client_id=client_id,
                total_cost=total_cost,
                balance=balance,
                status=status,
            )
            self.session.add(new_contract)
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
            return False

    def get_all(self):
        return self.session.query(Contract).all()

    def get_all_by_status(self, status):
        return self.session.query(Contract).filter(Contract.status == status).all()

    def get_all_by_user_responsibility(self, user_id):
        return (
            self.session.query(Contract)
            .join(Client)
            .filter(Client.user_id == user_id)
            .all()
        )

    def search(self, id):
        return self.session.query(Contract).filter(Contract.id == id).first()

    def update(self, contract_to_update):
        try:
            contract_in_db = (
                self.session.query(Contract).filter_by(id=contract_to_update.id).first()
            )
            if not contract_in_db:
                return False
            contract_in_db.user_id = contract_to_update.user_id
            contract_in_db.client_id = contract_to_update.client_id
            contract_in_db.total_cost = contract_to_update.total_cost
            contract_in_db.balance = contract_to_update.balance
            contract_in_db.status = contract_to_update.status
            contract_in_db.updating_date = datetime.datetime.now()
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
            return False

    def delete(self, contract_to_delete):
        contract_in_db = (
            self.session.query(Contract).filter_by(id=contract_to_delete.id).first()
        )
        if contract_in_db:
            self.session.delete(contract_to_delete)
            self.session.commit()
            return True
        else:
            return False
