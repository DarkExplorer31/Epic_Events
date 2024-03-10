"""Unit test for Event view"""

import unittest
from unittest.mock import patch, MagicMock
from views.eventview import EventView


class TestEventView(unittest.TestCase):
    def setUp(self):
        self.event_view = EventView()

    # Display methods tests
    @patch("views.eventview.display_green_message")
    @patch("views.eventview.display_red_message")
    def test_display_objects_with_objects(self, mock_red_message, mock_green_message):
        objects = ["object1", "object2", "object3"]
        self.event_view.display_objects(objects)
        mock_green_message.assert_called_once_with("Voici la liste des actuels:\n")
        self.assertEqual(mock_red_message.call_count, 0)

    @patch("views.eventview.display_green_message")
    @patch("views.eventview.display_red_message")
    def test_display_objects_with_empty_list(
        self, mock_red_message, mock_green_message
    ):
        objects = []
        self.event_view.display_objects(objects)
        mock_red_message.assert_called_once_with("Votre liste actuel est vide.\n")
        self.assertEqual(mock_green_message.call_count, 0)

    @patch("views.eventview.display_red_message")
    def test_display_contract_is_not_under_responsibility(
        self, mocked_display_red_message
    ):
        self.event_view.display_contract_is_not_under_responsibility()
        mocked_display_red_message.assert_called_with(
            "Le contrat n'est pas sous votre responsabilité."
        )

    @patch("views.eventview.display_red_message")
    def test_display_not_contract_exists(self, mocked_display_red_message):
        self.event_view.display_not_contract_exists()
        mocked_display_red_message.assert_called_once()

    @patch("views.eventview.display_red_message")
    def test_display_empty_list(self, mocked_display_red_message):
        self.event_view.display_empty_list()
        mocked_display_red_message.assert_called_once()

    @patch("views.eventview.display_red_message")
    def test_display_unfound_contract(self, mocked_display_red_message):
        self.event_view.display_unfound_contract()
        mocked_display_red_message.assert_called_once()

    @patch("views.eventview.display_green_message")
    def test_display_created(self, mocked_display_green_message):
        self.event_view.display_created()
        mocked_display_green_message.assert_called_with("L'événement a été créé.")

    @patch("views.eventview.display_red_message")
    def test_display_not_created(self, mocked_display_red_message):
        self.event_view.display_not_created()
        mocked_display_red_message.assert_called_once()

    @patch("views.eventview.display_red_message")
    def test_display_unfound_event(self, mocked_display_red_message):
        self.event_view.display_unfound_event()
        mocked_display_red_message.assert_called_once()

    @patch("views.eventview.display_red_message")
    def test_display_event_is_not_under_responsibility(
        self, mocked_display_red_message
    ):
        self.event_view.display_event_is_not_under_responsibility()
        mocked_display_red_message.assert_called_once()

    @patch("views.eventview.display_red_message")
    def test_display_unfound_support_user(self, mocked_display_red_message):
        self.event_view.display_unfound_support_user()
        mocked_display_red_message.assert_called_once()

    @patch("views.eventview.display_red_message")
    def test_display_unfound_support_user_in_db(self, mocked_display_red_message):
        self.event_view.display_unfound_support_user_in_db()
        mocked_display_red_message.assert_called_once()

    @patch("views.eventview.display_green_message")
    def test_display_event_is_update(self, mocked_display_green_message):
        self.event_view.display_event_is_update()
        mocked_display_green_message.assert_called_with("L'événement a été mis à jour.")

    @patch("views.eventview.display_red_message")
    def test_display_event_is_not_update(self, mocked_display_red_message):
        self.event_view.display_event_is_not_update()
        mocked_display_red_message.assert_called_with(
            "L'événement n'a pas été mis à jour."
        )

    # Searching methods tests
    @patch("views.eventview.Menu.information_menu")
    @patch("views.eventview.display_red_message")
    def test_search_event_with_valid_input(
        self, mock_red_message, mock_information_menu
    ):
        mock_information_menu.return_value = "123"
        result = self.event_view.search()
        self.assertEqual(result, 123)
        mock_red_message.assert_not_called()

    @patch("views.eventview.Menu.information_menu")
    @patch("views.eventview.display_red_message")
    def test_search_event_with_invalid_input(
        self, mock_red_message, mock_information_menu
    ):
        mock_information_menu.return_value = "invalid"
        result = self.event_view.search()
        self.assertIsNone(result)
        mock_red_message.assert_called_once_with("La valeur attendue est un chiffre.")

    @patch("views.eventview.Menu.information_menu")
    def test_search_support(self, mock_information_menu):
        mock_information_menu.return_value = "test@example.com"
        result = self.event_view.search_support()
        self.assertEqual(result, "test@example.com")

    # Get informations method tests
    @patch("views.eventview.Menu.information_menu")
    @patch("builtins.input")
    def test_get_new_event_information(self, mock_input, mock_information_menu):
        mock_input.side_effect = [
            "01/01/2024",
            "02/01/2024",
        ]
        mock_information_menu.side_effect = ["Paris", "10", "Some notes"]
        result = self.event_view.get_new_event_information()
        expected_result = {
            "starting_event_date": "01/01/2024",
            "ending_event_date": "02/01/2024",
            "location": "Paris",
            "attendees": 10,
            "notes": "Some notes",
        }
        self.assertEqual(result, expected_result)

    @patch("builtins.input")
    def test_get_new_event_information_failure(self, mock_input):
        mock_input.side_effect = ["01/01/2024", "q"]
        result = self.event_view.get_new_event_information()
        self.assertIsNone(result)

    # Update method test
    @patch("builtins.input")
    @patch("views.eventview.Menu.information_menu")
    def test_update_event_informations(self, mock_information_menu, mock_input):
        mock_input.side_effect = ["10/03/2024", "15/03/2024"]
        mock_information_menu.side_effect = ["Angers", "80", "Notes"]
        mocked_event = MagicMock()
        mocked_event.starting_event_date = "01/01/2024"
        mocked_event.ending_event_date = "05/01/2024"
        mocked_event.location = "Old Location"
        mocked_event.attendees = 5
        mocked_event.notes = "Old Notes"
        updated_event = self.event_view.update_event_informations(mocked_event)
        self.assertEqual(updated_event.starting_event_date, "10/03/2024")
        self.assertEqual(updated_event.ending_event_date, "15/03/2024")
        self.assertEqual(updated_event.location, "Angers")
        self.assertEqual(updated_event.attendees, 80)
        self.assertEqual(updated_event.notes, "Notes")

    @patch("views.eventview.Menu.global_menu")
    def test_choice_menu_event_manager(self, mock_global_menu):
        mock_global_menu.return_value = "t"
        user_role = "Manager"
        choice = self.event_view.choice_menu(user_role)
        expected_choice = "t"
        self.assertEqual(choice, expected_choice)

    @patch("views.eventview.Menu.global_menu")
    def test_choice_menu_event_support(self, mock_global_menu):
        mock_global_menu.return_value = "tf"
        user_role = "Support"
        choice = self.event_view.choice_menu(user_role)
        expected_choice = "tf"
        self.assertEqual(choice, expected_choice)

    @patch("views.eventview.Menu.global_menu")
    def test_choice_menu_event_sales(self, mock_global_menu):
        mock_global_menu.return_value = "a"
        user_role = "Sales"
        choice = self.event_view.choice_menu(user_role)
        expected_choice = "a"
        self.assertEqual(choice, expected_choice)


if __name__ == "__main__":
    unittest.main()
