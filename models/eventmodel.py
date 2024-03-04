"""Event model"""

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
            event_in_db.contact_id = event_to_update.contract_id
            event_in_db.starting_event_date = event_to_update.starting_event_date
            event_in_db.ending_event_date = event_to_update.ending_event_date
            event_in_db.support_contact_name = event_to_update.support_contact_name
            event_in_db.localisation = event_to_update.localisation
            event_in_db.attendees = event_to_update.attendees
            event_in_db.notes = event_to_update.notes
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
            return False
