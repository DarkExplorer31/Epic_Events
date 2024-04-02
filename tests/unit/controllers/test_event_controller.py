"""Unit test for Event manager"""

import unittest
from unittest.mock import MagicMock, patch

from controllers.eventmanager import EventManager
from views.eventview import EventView
from models.eventmodel import EventModel
from models.usermodel import UserModel
from models.contractmodel import ContractModel


class TestEventManager(unittest.TestCase):
    def setUp(self):
        self.mocked_session = MagicMock()
        self.mocked_user_authenticate = MagicMock()
        self.event_manager = EventManager(
            self.mocked_session, self.mocked_user_authenticate
        )
        self.event_view = MagicMock()
        self.event_model = MagicMock()
        self.contract_model = MagicMock()
        self.user_model = MagicMock()

    @patch.object(EventModel, "get_all")
    @patch.object(EventView, "display_objects")
    def test_get_all_events(self, mocked_display_objects, mocked_get_all):
        mocked_events = [{"id": 1, "name": "Event 1"}, {"id": 2, "name": "Event 2"}]
        mocked_get_all.return_value = mocked_events
        self.event_manager.get_all_events()
        mocked_display_objects.assert_called_once_with(mocked_events)

    @patch.object(EventModel, "get_all_non_attributed_events")
    @patch.object(EventModel, "get_all_attributed_events")
    @patch.object(EventModel, "get_all")
    def test_get_all_event_by_affectation(
        self,
        mocked_get_all,
        mocked_get_all_attributed_events,
        mocked_get_all_non_attributed_events,
    ):
        mocked_events = [{"id": 1, "name": "Event 1"}, {"id": 2, "name": "Event 2"}]
        mocked_get_all.return_value = mocked_events
        mocked_get_all_attributed_events.return_value = mocked_events
        mocked_get_all_non_attributed_events.return_value = mocked_events
        self.event_manager.role = "Manager"
        self.event_manager.get_all_event_by_affectation()
        mocked_get_all_non_attributed_events.assert_called_once()
        self.event_manager.role = "Support"
        self.event_manager.get_all_event_by_affectation()
        mocked_get_all_attributed_events.assert_called_once()

    @patch.object(ContractModel, "get_all_by_user_responsibility")
    @patch.object(EventView, "display_objects")
    def test_get_all_contract_by_affectation(
        self, mocked_display_objects, mocked_get_all_by_user_responsibility
    ):
        mocked_contracts = [
            {"id": 1, "name": "Contract 1"},
            {"id": 2, "name": "Contract 2"},
        ]
        mocked_get_all_by_user_responsibility.return_value = mocked_contracts
        self.event_manager.get_all_contract_by_affectation()
        mocked_display_objects.assert_called_once_with(mocked_contracts)

    @patch.object(UserModel, "get_all_support_user")
    @patch.object(EventView, "display_objects")
    @patch.object(EventView, "display_unfound_support_user")
    def test_get_all_support_user(
        self,
        mocked_display_unfound_support_user,
        mocked_display_objects,
        mocked_get_all_support_user,
    ):
        mocked_support_users = [
            {"id": 1, "name": "User 1"},
            {"id": 2, "name": "User 2"},
        ]
        mocked_get_all_support_user.return_value = mocked_support_users
        self.event_manager.get_all_support_user()
        mocked_display_objects.assert_called_once_with(mocked_support_users)
        mocked_display_objects.reset_mock()
        mocked_get_all_support_user.return_value = None
        self.event_manager.get_all_support_user()
        mocked_display_unfound_support_user.assert_called_once()

    @patch.object(EventManager, "get_all_contract_by_affectation")
    @patch.object(ContractModel, "search")
    @patch.object(EventView, "search")
    def test_select_contract_under_responsibility(
        self,
        mocked_search,
        mocked_contract_search,
        mocked_get_all_contract_by_affectation,
    ):
        mocked_contracts = [
            {"id": 1, "name": "Contract 1"},
            {"id": 2, "name": "Contract 2"},
        ]
        mocked_get_all_contract_by_affectation.return_value = mocked_contracts
        mocked_search.return_value = 1
        mocked_contract_search.return_value = {"id": 1, "name": "Contract 1"}
        self.event_manager.select_contract_under_responsibility()
        mocked_get_all_contract_by_affectation.assert_called_once()
        mocked_search.assert_called_once()
        mocked_contract_search.assert_called_once_with(id=1)

    @patch.object(EventManager, "get_all_event_by_affectation")
    @patch.object(EventModel, "search")
    @patch.object(EventView, "search")
    def test_select_event(
        self, mocked_search, mocked_event_search, mocked_get_all_event_by_affectation
    ):
        mocked_events = [{"id": 1, "name": "Event 1"}, {"id": 2, "name": "Event 2"}]
        mocked_get_all_event_by_affectation.return_value = mocked_events
        mocked_search.return_value = 1
        mocked_event_search.return_value = {"id": 1, "name": "Event 1"}
        self.event_manager.select_event()
        mocked_get_all_event_by_affectation.assert_called_once()
        mocked_search.assert_called_once()
        mocked_event_search.assert_called_once_with(id=1)

    @patch.object(EventManager, "get_all_support_user")
    @patch.object(UserModel, "search")
    @patch.object(EventView, "search_support")
    def test_select_support_to_assign(
        self, mocked_search_support, mocked_user_search, mocked_get_all_support_user
    ):
        mocked_users = [
            {"id": 1, "email": "user1@example.com"},
            {"id": 2, "email": "user2@example.com"},
        ]
        mocked_get_all_support_user.return_value = mocked_users
        mocked_search_support.return_value = "user1@example.com"
        mocked_user_search.return_value = {"id": 1, "email": "user1@example.com"}
        self.event_manager.select_support_to_assign()
        mocked_get_all_support_user.assert_called_once()
        mocked_search_support.assert_called_once()
        mocked_user_search.assert_called_once_with(loggin="user1@example.com")

    @patch.object(EventManager, "select_contract_under_responsibility")
    @patch.object(EventView, "get_new_event_information")
    @patch.object(EventModel, "create")
    @patch.object(EventView, "display_created")
    @patch.object(EventView, "display_not_created")
    def test_create_new_event(
        self,
        mocked_display_not_created,
        mocked_display_created,
        mocked_create,
        mocked_get_new_event_information,
        mocked_select_contract_under_responsibility,
    ):
        mocked_contract = MagicMock(id=1)
        mocked_select_contract_under_responsibility.return_value = mocked_contract
        mocked_get_new_event_information.return_value = {
            "starting_event_date": "2024-04-02",
            "ending_event_date": "2024-04-03",
            "location": "Location",
            "attendees": ["Attendee1", "Attendee2"],
            "notes": "Notes",
        }
        mocked_create.return_value = True
        self.event_manager.create_new_event()
        mocked_select_contract_under_responsibility.assert_called_once()
        mocked_get_new_event_information.assert_called_once()
        mocked_create.assert_called_once_with(
            contract_id=mocked_contract.id,
            starting_event_date="2024-04-02",
            ending_event_date="2024-04-03",
            location="Location",
            attendees=["Attendee1", "Attendee2"],
            notes="Notes",
        )
        mocked_display_created.assert_called_once()
        mocked_select_contract_under_responsibility.reset_mock()
        mocked_get_new_event_information.reset_mock()
        mocked_create.reset_mock()
        mocked_display_created.reset_mock()
        mocked_create.return_value = False
        self.event_manager.create_new_event()
        mocked_select_contract_under_responsibility.assert_called_once()
        mocked_get_new_event_information.assert_called_once()
        mocked_create.assert_called_once()
        mocked_display_not_created.assert_called_once()


if __name__ == "__main__":
    unittest.main()
