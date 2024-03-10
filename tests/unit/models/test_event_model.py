"""Unit test for Event model"""

import unittest
from datetime import datetime
from unittest.mock import MagicMock
from sqlalchemy.exc import IntegrityError

from models.eventmodel import EventModel, Event


class TestEventModel(unittest.TestCase):

    def setUp(self):
        self.session_mock = MagicMock()
        self.event_model = EventModel(self.session_mock)

    def test_create_event_success(self):
        contract_id = 1
        starting_event_date = "01/01/2023"
        ending_event_date = "02/01/2023"
        location = "New York"
        attendees = "John, Jane"
        notes = "Meeting notes"
        result = self.event_model.create(
            contract_id,
            starting_event_date,
            ending_event_date,
            location,
            attendees,
            notes,
        )
        self.assertTrue(result)
        self.session_mock.add.assert_called_once()
        self.session_mock.commit.assert_called_once()

    def test_create_event_failure(self):
        self.session_mock.add.side_effect = IntegrityError(
            "Integrity Error", params=None, orig=None
        )
        result = self.event_model.create(
            1, "01/01/2023", "02/01/2023", "New York", "John, Jane", "Meeting notes"
        )
        self.assertFalse(result)
        self.session_mock.rollback.assert_called_once()

    def test_get_all_events(self):
        result = self.event_model.get_all()
        self.assertEqual(result, self.session_mock.query(Event).all())

    def test_get_all_attributed_events(self):
        self.session_mock.query().filter().all.return_value = [Event(), Event()]
        result = self.event_model.get_all_attributed_events()
        self.assertEqual(len(result), 2)
        self.session_mock.query().filter().all.assert_called_once()

    def test_get_all_non_attributed_events(self):
        self.session_mock.query().filter().all.return_value = [Event(), Event()]
        result = self.event_model.get_all_non_attributed_events()
        self.assertEqual(len(result), 2)
        self.session_mock.query().filter().all.assert_called_once()

    def test_search_event_and_found(self):
        result = self.event_model.search(id=521)
        self.assertIsNotNone(result)

    def test_update_event(self):
        event_to_update = Event(
            id=1,
            contract_id=1,
            starting_event_date=datetime(2024, 3, 15),
            ending_event_date=datetime(2024, 3, 16),
            location="Location 1",
            attendees=10,
            notes="Notes 1",
        )
        self.session_mock.query().filter_by().first.return_value = event_to_update
        result = self.event_model.update(event_to_update)
        self.assertTrue(result)
        self.session_mock.commit.assert_called_once()

    def test_update_event_failure(self):
        event_to_update = Event(
            id=1,
            contract_id=1,
            starting_event_date=datetime(2024, 3, 15),
            ending_event_date=datetime(2024, 3, 16),
            location="Location 1",
            attendees=10,
            notes="Notes 1",
        )
        self.session_mock.query().filter_by().first.return_value = event_to_update
        self.session_mock.commit.side_effect = IntegrityError(
            "Integrity Error", params=None, orig=None
        )
        result = self.event_model.update(event_to_update)
        self.assertFalse(result)
        self.session_mock.query().filter_by().first.assert_called_once()
        self.session_mock.rollback.assert_called_once()


if __name__ == "__main__":
    unittest.main()
