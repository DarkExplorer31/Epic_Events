"""Unit test for User manager"""

import unittest
from unittest.mock import MagicMock, patch
from models.usermodel import UserModel
from views.userview import UserView
from controllers.usermanager import UserManager


class TestUserManager(unittest.TestCase):
    def setUp(self):
        self.mocked_session = MagicMock()
        self.mocked_user_authenticate = MagicMock()
        self.user_manager = UserManager(
            self.mocked_session, self.mocked_user_authenticate
        )

    @patch("controllers.usermanager.UserModel")
    @patch("controllers.usermanager.UserView")
    def test_init(self, mocked_user_view, mocked_user_model):
        user_manager = UserManager(self.mocked_session, self.mocked_user_authenticate)
        mocked_user_model.assert_called_once_with(self.mocked_session)
        mocked_user_view.assert_called_once()

    @patch("controllers.usermanager.UserModel.create")
    @patch("controllers.usermanager.UserView.get_new_user_information")
    @patch("controllers.usermanager.UserView.display_created")
    @patch("controllers.usermanager.UserView.display_not_created")
    def test_create_new_user(
        self,
        mocked_display_not_created,
        mocked_display_created,
        mocked_get_new_user_information,
        mocked_create,
    ):
        mocked_get_new_user_information.return_value = {
            "role": "Sales",
            "complete_name": "John Doe",
            "email": "john@example.com",
            "phone_number": "123456789",
            "password": "password",
        }
        self.user_manager.create_new_user()
        mocked_create.assert_called_once_with(
            role="Sales",
            complete_name="John Doe",
            email="john@example.com",
            phone_number="123456789",
            password="password",
        )
        mocked_display_created.assert_called_once()

    @patch("controllers.usermanager.UserModel.search")
    @patch("controllers.usermanager.UserView.search_user")
    @patch("controllers.usermanager.UserModel.get_all")
    @patch("controllers.usermanager.UserView.display_users")
    @patch("controllers.usermanager.UserView.display_unfound_user")
    def test_select_user(
        self,
        mocked_display_unfound_user,
        mocked_display_users,
        mocked_get_all,
        mocked_search_user,
        mocked_search,
    ):
        mocked_search_user.return_value = "john@example.com"
        mocked_get_all.return_value = ["user1", "user2", "user3"]
        mocked_search.return_value = "john@example.com"
        result = self.user_manager.select_user()
        mocked_get_all.assert_called_once()
        mocked_search_user.assert_called_once()
        mocked_search.assert_called_once_with(loggin="john@example.com")
        self.assertEqual(result, "john@example.com")
        mocked_display_users.assert_called_once_with(["user1", "user2", "user3"])
        mocked_display_unfound_user.assert_not_called()

    @patch("controllers.usermanager.UserManager.select_user", return_value=None)
    @patch("controllers.usermanager.UserView.get_update_user_informations")
    @patch("controllers.usermanager.UserModel.update")
    @patch("controllers.usermanager.UserView.display_user_is_not_update")
    def test_update_user_no_user_to_update(
        self,
        mocked_display_user_is_not_update,
        mocked_update,
        mocked_get_update_user_informations,
        mocked_select_user,
    ):
        self.assertIsNone(self.user_manager.update_user())
        mocked_select_user.assert_called_once()
        mocked_get_update_user_informations.assert_not_called()
        mocked_update.assert_not_called()
        mocked_display_user_is_not_update.assert_not_called()

    @patch("controllers.usermanager.UserManager.select_user", return_value=MagicMock())
    @patch(
        "controllers.usermanager.UserView.get_update_user_informations",
        return_value=MagicMock(),
    )
    @patch("controllers.usermanager.UserModel.update", return_value=True)
    @patch("controllers.usermanager.UserView.display_user_is_update")
    def test_update_user_successful(
        self,
        mocked_display_user_is_update,
        mocked_update,
        mocked_get_update_user_informations,
        mocked_select_user,
    ):
        self.user_manager.update_user()
        mocked_select_user.assert_called_once()
        mocked_get_update_user_informations.assert_called_once()
        mocked_update.assert_called_once()
        mocked_display_user_is_update.assert_called_once()

    @patch("controllers.usermanager.UserModel.delete")
    @patch("controllers.usermanager.UserModel.search")
    @patch("controllers.usermanager.UserView.search_user")
    @patch("controllers.usermanager.UserModel.get_all")
    @patch("controllers.usermanager.UserView.display_users")
    @patch("controllers.usermanager.UserView.display_user_is_delete")
    @patch("controllers.usermanager.UserView.display_user_is_not_delete")
    def test_delete_user(
        self,
        mocked_display_user_is_not_delete,
        mocked_display_user_is_delete,
        mocked_display_users,
        mocked_get_all,
        mocked_search_user,
        mocked_search,
        mocked_delete,
    ):
        mocked_user = MagicMock()
        mocked_user.id = 123
        mocked_search_user.return_value = "john@example.com"
        mocked_get_all.return_value = ["user1", "user2", "user3"]
        mocked_search.return_value = mocked_user
        mocked_delete.return_value = True
        self.user_manager.delete_user()
        mocked_get_all.assert_called_once()
        mocked_search_user.assert_called_once()
        mocked_search.assert_called_once_with(loggin="john@example.com")
        mocked_display_users.assert_called_once_with(["user1", "user2", "user3"])
        mocked_display_user_is_delete.assert_called_once()

    @patch("controllers.usermanager.UserView.choice_menu", return_value=None)
    @patch("controllers.usermanager.UserView.display_user_is_not_authorized")
    def test_menu_not_authorized(
        self, mocked_display_user_is_not_authorized, mocked_choice_menu
    ):
        self.user_manager.menu()
        mocked_display_user_is_not_authorized.assert_called_once()
        mocked_choice_menu.assert_called_once()

    @patch("controllers.usermanager.UserView.choice_menu", return_value="t")
    @patch("controllers.usermanager.UserManager.get_all_users")
    def test_menu_get_all_users(self, mocked_get_all_users, mocked_choice_menu):
        self.user_manager.menu()
        mocked_get_all_users.assert_called_once()
        mocked_choice_menu.assert_called_once()

    @patch("controllers.usermanager.UserManager.create_new_user")
    @patch("controllers.usermanager.UserView.choice_menu", return_value="a")
    def test_menu_create_new_user(self, mocked_choice_menu, mocked_create_new_user):
        self.user_manager.menu()
        mocked_choice_menu.assert_called_once()
        mocked_create_new_user.assert_called_once()

    @patch("controllers.usermanager.UserManager.update_user")
    @patch("controllers.usermanager.UserView.choice_menu", return_value="u")
    def test_menu_update_user(self, mocked_choice_menu, mocked_update_user):
        self.user_manager.menu()
        mocked_choice_menu.assert_called_once()
        mocked_update_user.assert_called_once()

    @patch("controllers.usermanager.UserManager.delete_user")
    @patch("controllers.usermanager.UserView.choice_menu", return_value="d")
    def test_menu_delete_user(self, mocked_choice_menu, mocked_delete_user):
        self.user_manager.menu()
        mocked_choice_menu.assert_called_once()
        mocked_delete_user.assert_called_once()


if __name__ == "__main__":
    unittest.main()
