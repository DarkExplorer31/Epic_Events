"""Unit test for User model"""

import unittest
from hashlib import sha256
from unittest.mock import MagicMock
from models.usermodel import UserModel
from models.db_models import User
from sqlalchemy.exc import IntegrityError


class TestUserModel(unittest.TestCase):

    def setUp(self):
        self.session_mock = MagicMock()
        self.user_model = UserModel(session=self.session_mock)

    def test_create_successful(self):
        result = self.user_model.create(
            role="ADMIN",
            complete_name="John Doe",
            email="john@example.com",
            phone_number="123456789",
            password="password",
        )
        self.assertTrue(result)
        self.session_mock.add.assert_called_once()
        self.session_mock.commit.assert_called_once()

    def test_create_user_integrity_error(self):
        self.session_mock.add.side_effect = IntegrityError(
            "Integrity Error", params=None, orig=None
        )
        result = self.user_model.create(
            role="ADMIN",
            complete_name="John Doe",
            email="john@example.com",
            phone_number="123456789",
            password="password",
        )
        self.assertFalse(result)
        self.session_mock.add.assert_called_once()
        self.session_mock.rollback.assert_called_once()

    def test_get_all_user(self):
        result = self.user_model.get_all()
        self.assertEqual(result, self.session_mock.query(User).all())

    def test_get_all_support_user(self):
        result = self.user_model.get_all_support_user()
        self.assertEqual(
            result, self.session_mock.query(User).filter_by(role="SUPPORT").all()
        )

    def test_search_and_found_a_user(self):
        result = self.user_model.search("john@example.com", "password")
        self.assertIsNotNone(result)

    def test_change_password(self):
        user_id = 1
        initial_password = "old_password"
        user_in_db_mock = MagicMock()
        user_in_db_mock.id = user_id
        user_in_db_mock.password = sha256(initial_password.encode()).hexdigest()
        user_in_db_mock.first_using_password = True
        self.session_mock.query.return_value.filter_by.return_value.first.return_value = (
            user_in_db_mock
        )
        new_password = "new_password"
        result = self.user_model.change_password(
            user_id=user_id, new_password=new_password
        )
        self.assertEqual(
            user_in_db_mock.password, sha256(new_password.encode()).hexdigest()
        )
        self.assertFalse(user_in_db_mock.first_using_password)
        self.assertTrue(result)

    def test_update_user(self):
        user_id = 1
        user_to_update_mock = MagicMock()
        user_to_update_mock.id = user_id
        updated_role = "ADMIN"
        updated_name = "Updated Name"
        updated_email = "updated_email@example.com"
        updated_phone_number = "987654321"
        user_to_update_mock.role = updated_role
        user_to_update_mock.complete_name = updated_name
        user_to_update_mock.email = updated_email
        user_to_update_mock.phone_number = updated_phone_number
        user_in_db_mock = MagicMock()
        user_in_db_mock.id = user_id
        self.session_mock.query.return_value.filter_by.return_value.first.return_value = (
            user_in_db_mock
        )
        result = self.user_model.update(user_to_update=user_to_update_mock)
        self.assertEqual(user_in_db_mock.role, updated_role)
        self.assertEqual(user_in_db_mock.complete_name, updated_name)
        self.assertEqual(user_in_db_mock.email, updated_email)
        self.assertEqual(user_in_db_mock.phone_number, updated_phone_number)
        self.assertTrue(result)

    def test_delete_user(self):
        user_id = 1
        user_in_db_mock = MagicMock()
        user_in_db_mock.id = user_id
        self.session_mock.query.return_value.filter_by.return_value.first.return_value = (
            user_in_db_mock
        )
        result = self.user_model.delete(user_id=user_id)
        self.session_mock.delete.assert_called_once_with(user_in_db_mock)
        self.session_mock.commit.assert_called_once()
        self.assertTrue(result)

    def test_not_delete_user(self):
        user_id = 1
        user_in_db_mock = MagicMock()
        user_in_db_mock.id = user_id
        self.session_mock.query.return_value.filter_by.return_value.first.return_value = (
            None
        )
        result = self.user_model.delete(user_id=user_id)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
