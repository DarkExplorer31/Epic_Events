"""Unit test for Client model"""

import unittest
from unittest.mock import MagicMock
from models.clientmodel import ClientModel
from models.db_models import Client
from sqlalchemy.exc import IntegrityError


class TestClientModel(unittest.TestCase):

    def setUp(self):
        self.session_mock = MagicMock()
        self.client_model = ClientModel(self.session_mock)

    def test_create_client_success(self):
        self.session_mock.add.return_value = None
        self.session_mock.commit.return_value = None

        result = self.client_model.create(
            user_id=1,
            complete_name="John Doe",
            email="john@example.com",
            phone_number="123456789",
            company_name="Company",
        )
        self.assertTrue(result)
        self.session_mock.add.assert_called_once()
        self.session_mock.commit.assert_called_once()

    def test_create_client_failure(self):
        self.session_mock.add.side_effect = IntegrityError(
            "Integrity Error", params=None, orig=None
        )
        self.session_mock.rollback.return_value = None
        result = self.client_model.create(
            user_id=1,
            complete_name="John Doe",
            email="john@example.com",
            phone_number="123456789",
            company_name="Company",
        )
        self.assertFalse(result)
        self.session_mock.add.assert_called_once()
        self.session_mock.rollback.assert_called_once()

    def test_get_all_clients(self):
        result = self.client_model.get_all()
        self.assertEqual(result, self.session_mock.query(Client).all())

    def test_search_client_and_found(self):
        result = self.client_model.search("john@example.com")
        self.assertIsNotNone(result)

    def test_update_client(self):
        client_to_update = Client(
            id=1,
            complete_name="John Doe",
            email="john@example.com",
            phone_number="123456789",
            company_name="ABC Inc.",
        )
        self.session_mock.query(Client).filter_by().first.return_value = (
            client_to_update
        )
        result = self.client_model.update(client_to_update)
        self.assertTrue(result)
        self.assertEqual(client_to_update.complete_name, "John Doe")
        self.assertEqual(client_to_update.email, "john@example.com")
        self.assertEqual(client_to_update.phone_number, "123456789")
        self.assertEqual(client_to_update.company_name, "ABC Inc.")
        self.assertIsNotNone(client_to_update.updating_date)
        self.session_mock.commit.assert_called_once()

    def test_delete_client(self):
        client_to_delete = Client(email="john@example.com")
        self.session_mock.query(Client).filter_by().first.return_value = (
            client_to_delete
        )
        result = self.client_model.delete(client_to_delete)
        self.assertTrue(result)
        self.session_mock.delete.assert_called_once_with(client_to_delete)
        self.session_mock.commit.assert_called_once()

    def test_delete_client_not_found(self):
        client_to_delete = Client(email="john@example.com")
        self.session_mock.query.return_value.filter_by.return_value.first.return_value = (
            None
        )
        result = self.client_model.delete(client_to_delete)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
