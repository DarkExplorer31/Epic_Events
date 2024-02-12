"""Authentication controller"""

from views.userview import UserView
from models.user import User


class AuthenticationController:
    def __init__(self):
        self.view = UserView()
        self.user = User()

    def authenticate(self, username, password):
        pass
