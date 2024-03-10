"""Unit test for Contract model"""

import unittest
from unittest.mock import MagicMock
from models.contractmodel import ContractModel
from models.db_models import Contract, StatusEnum
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


class TestContractModel(unittest.TestCase):
    def setUp(self):
        self.session_mock = MagicMock()
        self.contract_model = ContractModel(self.session_mock)

    def test_create_contract(self):
        new_contract = Contract(
            user_id=1,
            client_id=1,
            total_cost=1000,
            balance=500,
            status=StatusEnum.UNPAID,
        )
        result = self.contract_model.create(
            user_id=new_contract.user_id,
            client_id=new_contract.client_id,
            total_cost=new_contract.total_cost,
            balance=new_contract.balance,
            status=new_contract.status,
        )
        self.assertTrue(result)
        self.session_mock.add.assert_called_once()
        self.session_mock.commit.assert_called_once()

    def test_get_all_contracts(self):
        result = self.contract_model.get_all()
        self.assertEqual(result, self.session_mock.query(Contract).all())

    def test_search_contract_found(self):
        expected_contract = Contract(
            id=1, user_id=1, client_id=1, total_cost=100, balance=50, status="Active"
        )
        self.session_mock.query().filter().first.return_value = expected_contract
        result = self.contract_model.search(id=1)
        self.assertEqual(result, expected_contract)

    def test_search_contract_not_found(self):
        self.session_mock.query().filter().first.return_value = None
        result = self.contract_model.search(id=1)
        self.assertIsNone(result)

    def test_search_contract_error(self):
        self.session_mock.query().filter().first.side_effect = SQLAlchemyError(
            "Database connection error"
        )
        with self.assertRaises(SQLAlchemyError):
            self.contract_model.search(id=1)

    def test_update_contract(self):
        contract_to_update = Contract(
            id=1,
            user_id=1,
            client_id=1,
            total_cost=1000,
            balance=500,
            status=StatusEnum.UNPAID,
        )
        self.session_mock.query(Contract).filter_by().first.return_value = (
            contract_to_update
        )
        result = self.contract_model.update(contract_to_update)
        self.assertTrue(result)
        self.assertEqual(contract_to_update.user_id, 1)
        self.assertEqual(contract_to_update.client_id, 1)
        self.assertEqual(contract_to_update.total_cost, 1000)
        self.assertEqual(contract_to_update.balance, 500)
        self.assertEqual(contract_to_update.status, StatusEnum.UNPAID)
        self.assertIsNotNone(contract_to_update.updating_date)

    def test_update_contract_failure(self):
        contract_to_update = Contract(
            id=1,
            user_id=1,
            client_id=1,
            total_cost=1000,
            balance=500,
            status=StatusEnum.UNPAID,
        )
        self.session_mock.query().filter_by().first.return_value = contract_to_update
        self.session_mock.commit.side_effect = IntegrityError(
            "Integrity Error", params=None, orig=None
        )
        result = self.contract_model.update(contract_to_update)
        self.assertFalse(result)
        self.session_mock.query().filter_by().first.assert_called_once()
        self.session_mock.rollback.assert_called_once()

    def test_delete_contract(self):
        contract_to_delete = Contract(id=17)
        self.session_mock.query(Contract).filter_by().first.return_value = (
            contract_to_delete
        )
        result = self.contract_model.delete(contract_to_delete)
        self.assertTrue(result)
        self.session_mock.delete.assert_called_once_with(contract_to_delete)
        self.session_mock.commit.assert_called_once()

    def test_delete_contract_not_found(self):
        contract_to_delete = contract_to_delete = Contract(id=17)
        self.session_mock.query.return_value.filter_by.return_value.first.return_value = (
            None
        )
        result = self.contract_model.delete(contract_to_delete)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
