"""Event model"""

from sqlalchemy.exc import IntegrityError

from .db_models import Event


class EventModel:
    def __init__(self, session):
        self.session = session

    def create_event(self, contract, informations):
        try:
            new_event = Event(
                contract_id=contract,
                starting_event_date=informations[0],
                ending_event_date=informations[1],
                support_contact_name=informations[2],
                localisation=informations[3],
                attendees=informations[4],
                notes=informations[5],
            )
            self.session.add(new_event)
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
            return False

    def get_all_events(self):
        events = self.session.query(Event)
        return events

    def search_event(self, id):
        if id:
            event = self.session.query(Event).filter(Event.id == id).first()
            if event:
                return event
            else:
                return None
        else:
            return None

    def update_event(self, event_to_update):
        """Update an Event in Database"""
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

    def delete_event(self, event_to_delete):
        event_in_db = self.session.query(Event).filter_by(id=event_to_delete.id).first()
        if event_in_db:
            self.session.delete(event_to_delete)
            self.session.commit()
            return True
        else:
            return False
