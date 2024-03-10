"""Event manager"""

from models.eventmodel import EventModel
from models.contractmodel import ContractModel
from models.usermodel import UserModel
from views.eventview import EventView


class EventManager:

    def __init__(self, session, user_authenticate):
        self.model = EventModel(session)
        self.contract_model = ContractModel(session)
        self.user_model = UserModel(session)
        self.view = EventView()
        self.role = user_authenticate.role.value
        self.user_id = user_authenticate.id

    # Obtaining methods
    def get_all_events(self):
        all_events = self.model.get_all()
        self.view.display_objects(all_events)
        if not all_events:
            return None
        return all_events

    def get_all_event_by_affectation(self):
        if self.role == "Manager":
            all_events = self.model.get_all_non_attributed_events()
        elif self.role == "Support":
            all_events = self.model.get_all_attributed_events()
        else:
            all_events = self.get_all_events()
        if not all_events:
            self.view.display_empty_list()
            return None
        self.view.display_objects(all_events)
        return all_events

    def get_all_contract_by_affectation(self):
        all_contracts = self.contract_model.get_all_by_user_responsibility(self.user_id)
        if not all_contracts:
            return None
        self.view.display_objects(all_contracts)
        return all_contracts

    def get_all_support_user(self):
        all_support_user = self.user_model.get_all_support_user()
        if not all_support_user:
            self.view.display_unfound_support_user()
            return None
        self.view.display_objects(all_support_user)
        return all_support_user

    # Searching methods
    def select_contract_under_responsibility(self):
        contracts_to_display = self.get_all_contract_by_affectation()
        if not contracts_to_display:
            self.view.display_not_contract_exists()
            return None
        search_id = self.view.search()
        contract = self.contract_model.search(id=search_id)
        if not contract:
            self.view.display_unfound_contract()
        return contract

    def select_event(self):
        events_to_display = self.get_all_event_by_affectation()
        if not events_to_display:
            return None
        search_id = self.view.search()
        event = self.model.search(id=search_id)
        if not event:
            self.view.display_unfound_event()
        return event

    def select_support_to_assign(self):
        users_to_display = self.get_all_support_user()
        if not users_to_display:
            return None
        email = self.view.search_support()
        support_user = self.user_model.search(loggin=email)
        if not support_user:
            self.view.display_unfound_support_user_in_db()
        return support_user

    # Create method
    def create_new_event(self):
        concerned_contract = self.select_contract_under_responsibility()
        if not concerned_contract:
            return None
        data = self.view.get_new_event_information()
        if not data:
            return None
        creation = self.model.create(
            contract_id=concerned_contract.id,
            starting_event_date=data["starting_event_date"],
            ending_event_date=data["ending_event_date"],
            location=data["location"],
            attendees=data["attendees"],
            notes=data["notes"],
        )
        if creation:
            self.view.display_created()
        else:
            self.view.display_not_created()

    # Update method
    def update_event(self):
        event_to_update = self.select_event()
        if not event_to_update:
            return None
        elif event_to_update.support_id == self.user_id:
            event_to_update = self.view.update_event_informations(event_to_update)
        elif self.role == "Manager":
            selected_support = self.select_support_to_assign()
            if not selected_support:
                return None
            event_to_update.support_id = selected_support.id
        else:
            self.view.display_event_is_not_under_responsibility()
            return None
        update = self.model.update(event_to_update)
        if update:
            self.view.display_event_is_update()
        else:
            self.view.display_event_is_not_update()

    # Main method
    def menu(self):
        choice = self.view.choice_menu(self.role)
        if not choice:
            return None
        if choice == "t":
            self.get_all_events()
        elif choice == "tf" and self.role in ["Manager", "Support"]:
            self.get_all_event_by_affectation()
        elif choice == "a" and self.role == "Sales":
            self.create_new_event()
        elif choice == "u" and self.role in ["Manager", "Support"]:
            self.update_event()
        elif choice == "q":
            return None
