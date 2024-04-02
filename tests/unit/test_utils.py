"""Unit test for utils.py"""

import unittest
from unittest.mock import patch
import string
from utils import generate_password, Menu


class TestGeneratePassword(unittest.TestCase):
    def test_password_length(self):
        password = generate_password(length=10)
        self.assertEqual(len(password), 10)

    def test_special_characters(self):
        password = generate_password(length=12)
        special_characters = set(string.punctuation)
        self.assertTrue(any(char in special_characters for char in password))

    def test_alphanumeric_characters(self):
        password = generate_password(length=12)
        self.assertTrue(any(char.isalnum() for char in password))

    def test_uniqueness(self):
        password1 = generate_password()
        password2 = generate_password()
        self.assertNotEqual(password1, password2)


class TestMenu(unittest.TestCase):
    def setUp(self):
        self.menu = Menu()

    @patch("builtins.input", return_value="1")
    def test_menu_valid_choice(self, mock_input):
        options = {"1": "Option 1", "2": "Option 2"}
        choice = self.menu.global_menu(options)
        self.assertEqual(choice, "1")

    def test_menu_exit_choice(self):
        options = {"1": "Option 1", "2": "Option 2"}
        with patch("builtins.input", return_value="q"):
            choice = self.menu.global_menu(options)
        self.assertEqual(choice, "q")

    def test_menu_invalid_options(self):
        invalid_options = "not a dictionary"
        with self.assertRaises(ValueError):
            self.menu.global_menu(invalid_options)

    @patch("builtins.input", return_value="1")
    def test_menu_valid_choice(self, mock_input):
        choice = self.menu.information_menu(
            "Choose an option:", possible_response=["1", "2", "3"]
        )
        self.assertEqual(choice, "1")

    @patch("builtins.input", side_effect=["q"])
    def test_menu_exit_choice(self, mock_input):
        choice = self.menu.information_menu("Choose an option:")
        self.assertIsNone(choice)

    @patch("builtins.input", side_effect=["invalid", "2"])
    def test_menu_invalid_choice(self, mock_input):
        choice = self.menu.information_menu(
            "Choose an option:", possible_response=["1", "2", "3"]
        )
        self.assertEqual(choice, "2")

    @patch("builtins.input", side_effect=["invalid", "option 2"])
    @patch("utils.display_red_message")
    def test_menu_not_conform_message(self, mock_display_red_message, mock_input):
        choice = self.menu.information_menu(
            "Choose an option:",
            value_in_sentence="option",
            not_conform_message="Value does not contain 'option'",
        )
        mock_display_red_message.assert_called_once()
        self.assertEqual(choice, "option 2")

    @patch("utils.Menu.global_menu", return_value="t")
    def test_menu_crud_menu_view(self, mock_global_menu):
        choice = self.menu.crud_menu("item")
        self.assertEqual(choice, "t")

    @patch("utils.Menu.global_menu", return_value="a")
    def test_menu_crud_menu_add(self, mock_global_menu):
        choice = self.menu.crud_menu("item")
        self.assertEqual(choice, "a")

    @patch("utils.Menu.global_menu", return_value="q")
    def test_menu_crud_menu_quit(self, mock_global_menu):
        choice = self.menu.crud_menu("item")
        self.assertIsNone(choice)

    @patch("utils.Menu.global_menu", return_value="t")
    def test_menu_no_permission_menu_view(self, mock_global_menu):
        choice = self.menu.no_permission_menu("item")
        self.assertEqual(choice, "t")

    @patch("utils.Menu.global_menu", return_value="q")
    def test_menu_no_permission_menu_quit(self, mock_global_menu):
        choice = self.menu.no_permission_menu("item")
        self.assertIsNone(choice)


if __name__ == "__main__":
    unittest.main()
