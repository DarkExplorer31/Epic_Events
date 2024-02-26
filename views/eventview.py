"""Event view"""

import re

from utils import Menu, display_green_message, display_red_message


class EventView:
    DATE_TYPE = r"^[0-9]{2}/[0-9]{2}/[0-9]{4}$"

    def __init__(self):
        self.menu = Menu()

    def display_all_events(self, all_events):
        if all_events:
            display_green_message("Voici la liste des évènements:\n")
            for contrat in all_events:
                print(contrat)
        else:
            display_red_message("Votre liste d'évènement est vide.\n")

    def add_new_event_view(self):
        print(f"Bienvenue dans la création d'un nouvel évènement\n")
        while True:
            starting_event_date = input(
                "Entrez la date de début de l'évènement (au format JJ/MM/AAAA) ou 'q' pour quitter\n> "
            )
            if not starting_event_date or starting_event_date == "q":
                return None
            elif re.match(self.DATE_TYPE, starting_event_date):
                display_green_message("Le format de la date est bonne.")
            else:
                display_red_message("Le format doit être JJ/MM/AAAA.")
                continue
            ending_event_date = input(
                "Entrez la date de fin de l'évènement (au format JJ/MM/AAAA)"
                + " ou 'q' pour quitter\n> "
            )
            if not ending_event_date or ending_event_date == "q":
                return None
            elif re.match(self.DATE_TYPE, ending_event_date):
                display_green_message("Le format de la date est bonne.")
            else:
                display_red_message("Le format doit être JJ/MM/AAAA.")
                continue
            support_name = self.menu.information_menu(
                asking_sentence="Veuillez remplir le nom du support"
            )
            if not support_name:
                return None
            localisation = self.menu.information_menu(
                asking_sentence="Veuillez remplir le lieux"
            )
            if not localisation:
                return None
            attendees = self.menu.information_menu(
                asking_sentence="Veuillez remplir le nombre de participant"
            )
            if not attendees:
                return None
            try:
                attendees = int(attendees)
            except ValueError:
                display_red_message("Ce champs attend un nombre")
            if attendees <= 0:
                display_red_message(
                    "Le nombre de participant ne peut pas être vide ou négatif."
                )
                continue
            notes = self.menu.information_menu(
                asking_sentence="Veuillez remplir un commentaire si besoin"
            )
            return [
                starting_event_date,
                ending_event_date,
                support_name,
                localisation,
                attendees,
                notes,
            ]

    def find_event(self):
        print(f"Bienvenue dans la fonction de recherche d'un évènement")
        id = self.menu.information_menu(
            asking_sentence="Veuillez renseigner l'id de l'évènement",
        )
        if not id:
            return None
        try:
            id = int(id)
        except ValueError:
            display_red_message("La valeur attendue est un chiffre.")
            return None
        return id

    def update_event_informations_view(self, event):
        print(
            "\n"
            + f"Vous voulez mettre à jour les informations de l'évènement {event.id}."
            + f"L'évènement à été créer le: {event.creation_date}"
            + "\n"
        )
        starting_event_date = input(
            "Entrez la date de début de l'évènement (au format JJ/MM/AAAA) ou 'q' pour quitter\n> "
        )
        if not starting_event_date or starting_event_date == "q":
            display_red_message("Pas de modification.")
        elif re.match(self.DATE_TYPE, starting_event_date):
            display_green_message("La date  été changé.")
            event.starting_event_date = starting_event_date
        else:
            display_red_message("Le format doit être JJ/MM/AAAA.")
        ending_event_date = input(
            "Entrez la date de fin de l'évènement (au format JJ/MM/AAAA)"
            + " ou 'q' pour quitter\n> "
        )
        if not ending_event_date or ending_event_date == "q":
            display_red_message("Pas de modification.")
        elif re.match(self.DATE_TYPE, ending_event_date):
            display_green_message("La date  été changé.")
            event.ending_event_date = ending_event_date
        else:
            display_red_message("Le format doit être JJ/MM/AAAA.")
        localisation = self.menu.information_menu(
            asking_sentence="Veuillez remplir le lieux"
        )
        if not localisation or localisation == event.localisation:
            display_red_message("Pas de modification.")
        else:
            event.localisation = localisation
        attendees = self.menu.information_menu(
            asking_sentence="Veuillez remplir le nombre de participant"
        )
        if not attendees or attendees == event.attendees:
            display_red_message("Pas de modification.")
        try:
            attendees = int(attendees)
        except ValueError:
            display_red_message("Ce champs attend un nombre")
        if attendees <= 0:
            display_red_message(
                "Le nombre de participant ne peut pas être vide ou négatif."
            )
        else:
            event.attendees = attendees
        notes = self.menu.information_menu(
            asking_sentence="Veuillez remplir un commentaire si besoin"
        )
        if notes == event.notes or not notes:
            display_red_message("Pas de modification.")
        else:
            event.notes = notes
        return event

    def update_support_assignated_view(self, event):
        print(
            "\n"
            + f"Vous voulez mettre à jour les informations de l'évènement {event.id}."
            + f"L'évènement à été créer le: {event.creation_date}"
            + "\n"
            + f"il est attribué à: {event.support_contact_name}"
            + "\n"
        )
        support_name = self.menu.information_menu(
            asking_sentence="Veuillez remplir le nom du support"
        )
        if not support_name or support_name == event.support_name:
            display_red_message("Pas de modification.")
        else:
            event.support_name = support_name
        return event
