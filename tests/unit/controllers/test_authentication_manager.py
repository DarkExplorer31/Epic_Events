"""Authentication manager unit test"""

import unittest
from unittest.mock import patch, MagicMock
from views.authenticationview import AuthenticationView
from controllers.authenticationmanager import AuthenticationController
from utils import Menu


class TestAuthenticationController(unittest.TestCase):

    @patch("controllers.authenticationmanager.AuthenticationView.ask_authentication")
    @patch("controllers.authenticationmanager.UserModel.search")
    def test_authenticate_successful(self, mocked_search, mocked_ask_authentication):
        mocked_ask_authentication.return_value = {
            "login": "user",
            "password": "password",
        }
        mocked_search.return_value = MagicMock(first_using_password=False)
        auth_controller = AuthenticationController(session=None)
        result = auth_controller.authenticate()
        self.assertIsNotNone(result)
        mocked_ask_authentication.assert_called_once()
        mocked_search.assert_called_once_with("user", "password")

    @patch("controllers.authenticationmanager.AuthenticationView.ask_authentication")
    @patch("controllers.authenticationmanager.UserModel.search")
    def test_authenticate_unsuccessful(self, mocked_search, mocked_ask_authentication):
        mocked_ask_authentication.return_value = {
            "login": "user",
            "password": "password",
        }
        mocked_search.return_value = None
        auth_controller = AuthenticationController(session=None)
        result = auth_controller.authenticate()
        self.assertIsNone(result)
        mocked_ask_authentication.assert_called_once()
        mocked_search.assert_called_once_with("user", "password")

    @patch("controllers.authenticationmanager.AuthenticationView.ask_authentication")
    @patch("controllers.authenticationmanager.UserModel.search")
    @patch("controllers.authenticationmanager.AuthenticationView.add_new_password")
    @patch("controllers.authenticationmanager.UserModel.change_password")
    def test_authenticate_change_password(
        self,
        mocked_change_password,
        mocked_add_new_password,
        mocked_search,
        mocked_ask_authentication,
    ):
        mocked_ask_authentication.return_value = {
            "login": "user",
            "password": "password",
        }
        mocked_search.return_value = MagicMock(
            first_using_password=True, id=1, password="oldpassword"
        )
        mocked_add_new_password.return_value = "newpassword"
        mocked_change_password.return_value = True
        auth_controller = AuthenticationController(session=None)
        result = auth_controller.authenticate()
        self.assertIsNotNone(result)
        mocked_ask_authentication.assert_called_once()
        mocked_search.assert_called_once_with("user", "password")
        mocked_add_new_password.assert_called_once_with("oldpassword")
        mocked_change_password.assert_called_once_with(1, "newpassword")

    @patch("controllers.authenticationmanager.AuthenticationView.ask_authentication")
    @patch("controllers.authenticationmanager.UserModel.search")
    def test_authenticate_failed(self, mocked_search, mocked_ask_authentication):
        mocked_ask_authentication.return_value = None
        auth_controller = AuthenticationController(session=None)
        result = auth_controller.authenticate()
        self.assertIsNone(result)
        mocked_ask_authentication.assert_called_once()
        mocked_search.assert_not_called()

    @patch("controllers.authenticationmanager.AuthenticationView.display_hello_user")
    @patch("controllers.authenticationmanager.AuthenticationView.select_menu_by_role")
    def test_main_menu_successful(
        self, mocked_select_menu_by_role, mocked_display_hello_user
    ):
        mocked_select_menu_by_role.return_value = "u"
        user_mock = MagicMock()
        auth_controller = AuthenticationController(session=None)
        result = auth_controller.main_menu(user_mock)
        self.assertEqual(result, "u")
        mocked_display_hello_user.assert_called_once_with(user_mock)
        mocked_select_menu_by_role.assert_called_once_with(user_mock)

    @patch("controllers.authenticationmanager.AuthenticationView.display_hello_user")
    @patch("controllers.authenticationmanager.AuthenticationView.select_menu_by_role")
    def test_main_menu_with_bad_value(
        self, mocked_select_menu_by_role, mocked_display_hello_user
    ):
        mocked_select_menu_by_role.return_value = "tred"
        user_mock = MagicMock()
        auth_controller = AuthenticationController(session=None)
        result = auth_controller.main_menu(user_mock)
        self.assertNotEqual(result, "u")
        mocked_display_hello_user.assert_called_once_with(user_mock)
        mocked_select_menu_by_role.assert_called_once_with(user_mock)


if __name__ == "__main__":
    unittest.main()
