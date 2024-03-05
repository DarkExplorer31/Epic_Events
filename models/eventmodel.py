"""Event model"""

from datetime import datetime
from sqlalchemy.exc import IntegrityError

from .db_models import Event


class EventModel:
    def __init__(self, session):
        self.session = session

    def create(
        self,
        contract_id,
        starting_event_date,
        ending_event_date,
        location,
        attendees,
        notes,
        support_id=None,
    ):
        try:
            starting_event_date = datetime.strptime(starting_event_date, "%d/%m/%Y")
            ending_event_date = datetime.strptime(ending_event_date, "%d/%m/%Y")
            new_event = Event(
                contract_id=contract_id,
                support_id=support_id,
                starting_event_date=starting_event_date,
                ending_event_date=ending_event_date,
                location=location,
                attendees=attendees,
                notes=notes,
            )
            self.session.add(new_event)
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
            return False

    def get_all(self):
        return self.session.query(Event).all()

    def get_all_attributed_events(self):
        return self.session.query(Event).filter(Event.support_id != None).all()

    def get_all_non_attributed_events(self):
        return self.session.query(Event).filter(Event.support_id == None).all()

    def search(self, id):
        return self.session.query(Event).filter(Event.id == id).first()

    def update(self, event_to_update):
        try:
            event_in_db = (
                self.session.query(Event).filter_by(id=event_to_update.id).first()
            )
            if not event_in_db:
                return False
            if isinstance(event_in_db.starting_event_date, str):
                event_in_db.starting_event_date = datetime.strptime(
                    event_in_db.starting_event_date, "%d/%m/%Y"
                )
            elif isinstance(event_in_db.ending_event_date, str):
                event_in_db.ending_event_date = datetime.strptime(
                    event_in_db.ending_event_date, "%d/%m/%Y"
                )
            event_in_db.contact_id = event_to_update.contract_id
            event_in_db.support_id = event_to_update.support_id
            event_in_db.starting_event_date = event_to_update.starting_event_date
            event_in_db.ending_event_date = event_to_update.ending_event_date
            event_in_db.location = event_to_update.location
            event_in_db.attendees = event_to_update.attendees
            event_in_db.notes = event_to_update.notes
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
            return False
