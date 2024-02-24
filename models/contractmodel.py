"""Contract model"""

import datetime
from sqlalchemy.exc import IntegrityError

from .db_models import Contract


class ContractModel:
    def __init__(self, session):
        self.session = session

    def create_contract(self, current_user, client, informations):
        try:
            new_contract = Contract(
                user_id=current_user,
                client_id=client,
                total_cost=informations[0],
                balance=informations[1],
                status=informations[2],
            )
            self.session.add(new_contract)
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
            return False

    def get_all_contracts(self):
        contracts = self.session.query(Contract)
        return contracts

    def search_contract(self, id):
        if id:
            contract = (
                self.session.query(Contract)
                .filter(
                    Contract.id == id).first())
            if contract:
                return contract
            else:
                return None
        else:
            return None

    def update_contract(self,contract_to_update):
        """Update a Contract in Database"""
        contract_in_db = self.session.query(Contract).filter_by(id=contract_to_update.id).first()
        if contract_in_db:
            try:
                contract_in_db.user_id = contract_to_update.user_id
                contract_in_db.client_id = contract_to_update.client_id
                contract_in_db.total_cost = contract_to_update.total_cost
                contract_in_db.balance = contract_to_update.balance
                contract_in_db.status = contract_to_update.status
                contract_in_db.updating_date = datetime.now
                self.session.commit()
                return True
            except IntegrityError:
                self.session.rollback()
                return False
        else:
            return False

    def delete_contract(self, contract_to_delete):
        contract_in_db = self.session.query(Contract).filter_by(id=contract_to_delete.id).first()
        if contract_in_db:
            self.session.delete(contract_to_delete)
            self.session.commit()
            return True
        else:
            return False