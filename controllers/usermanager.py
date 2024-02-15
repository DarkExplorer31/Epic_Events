"""User manager"""

from views.userview import UserView
from models.user import User


class UserManager:
    def __init__(self, session, current_user):
        self.view = UserView()
        self.current_user = current_user
        self.session = session

    def add_new_user(self, username):
        """Only for management member, this method add a new colaborator"""
        informations = self.view.add_new_user_view(username)
        new_user = User(
            role=informations[0],
            complete_name=informations[1],
            email=informations[2],
            phone_number=informations[3],
            password=informations[4],
        )
        self.session.add(new_user)
        self.session.commit()

    def update_user_information(self):
        """Only for management member, this method update colaborator's information"""

    def delete_user(self):
        """Only for management member, this method delete a colaborator in db"""

    def run(self):
        pass
