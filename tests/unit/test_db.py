"""Unit test for db.py"""

import unittest
from unittest.mock import patch
from db import DataBase


class TestDataBase(unittest.TestCase):
    def setUp(self):
        self.db = DataBase()

    @patch("db.create_engine")
    @patch("db.sessionmaker")
    @patch("db.Base.metadata.create_all")
    def test_create_db_session_success(
        self, mock_create_all, mock_sessionmaker, mock_create_engine
    ):
        session = self.db.create_db_session()
        self.assertIsNotNone(session)
        mock_create_all.assert_called_once()
        mock_sessionmaker.assert_called_once_with(bind=mock_create_engine.return_value)

    @patch("db.create_engine")
    @patch("db.Base.metadata.create_all", side_effect=Exception("Test Exception"))
    def test_create_db_session_failure(self, mock_create_all, mock_create_engine):
        with self.assertRaises(Exception):
            self.db.create_db_session()
        mock_create_all.assert_called_once()
        mock_create_engine.assert_called_once()


if __name__ == "__main__":
    unittest.main()
