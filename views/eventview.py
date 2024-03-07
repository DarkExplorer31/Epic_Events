"""Event view"""

import re

from utils import Menu, display_green_message, display_red_message


class EventView:
    DATE_TYPE = r"^[0-3][0-9]/[0-1][0-9]/[0-9]{4}$"

    def __init__(self):
        self.menu = Menu()

    # Displaying methods
    def display_objects(self, objects):
        if objects:
            display_green_message("Voici la liste des actuels:\n")
            for object in objects:
                print(f"-{object}")
        else:
            display_red_message("Votre liste actuel est vide.\n")

    def display_contract_is_not_under_responsibility(self):
        display_red_message("Le contrat n'est pas sous votre responsabilité.")

    def display_not_contract_exists(self):
        display_red_message(
            "Il n'existe aucun contrat. "
            + "Il vous faut un contrat pour pouvoir créer une événement."
        )

    def display_empty_list(self):
        display_red_message("Votre liste d'événement filtré est vide.")

    def display_unfound_contract(self):
        display_red_message("Le contrat n'a pas été trouvé.")

    def display_created(self):
        display_green_message("L'événement a été créé.")

    def display_not_created(self):
        display_red_message("L'événement n'a pas été créé.")

    def display_unfound_event(self):
        display_red_message("L'événement n'a pas été trouvé.")

    def display_event_is_not_under_responsibility(self):
        display_red_message("L'événement n'est pas sous votre responsabilité.")

    def display_unfound_support_user(self):
        display_red_message(
            "Aucun utilisateur support n'a été trouvé. Vous"
            + " devez en créer un pour pouvoir l'assigner à un événement."
        )

    def display_unfound_support_user_in_db(self):
        display_red_message(
            "L'utilisateur support n'a pas été trouvé dans la base de donnée."
        )

    def display_event_is_update(self):
        display_green_message("L'événement a été mis à jour.")

    def display_event_is_not_update(self):
        display_red_message("L'événement n'a pas été mis à jour.")

    # Searching methods
    def search(self):
        print("Bienvenue dans la fonction de recherche")
        id = self.menu.information_menu(
            asking_sentence="Veuillez renseigner l'id a recherché",
        )
        if not id:
            return None
        try:
            id = int(id)
        except ValueError:
            display_red_message("La valeur attendue est un chiffre.")
            return None
        return id

    def search_support(self):
        print("Bienvenue dans la fonction de recherche d'un support")
        email = self.menu.information_menu(
            asking_sentence="Veuillez remplir son email",
            value_in_sentence=self.EMAIL_TYPE,
            not_conform_message="L'email doit comporter un '@'",
        )
        return email

    # Get informations method
    def get_new_event_information(self):
        print("Bienvenue dans la création d'un nouvel événement\n")
        while True:
            starting_event_date = input(
                "Entrez la date de début de l'événement (au format JJ/MM/AAAA) ou 'q' pour quitter\n> "
            )
            if not starting_event_date or starting_event_date == "q":
                return None
            elif re.match(self.DATE_TYPE, starting_event_date):
                display_green_message("Le format de la date est bonne.")
            else:
                display_red_message(
                    "Le format doit être JJ/MM/AAAA"
                    + " et doit être une date cohérente."
                )
                continue
            ending_event_date = input(
                "Entrez la date de fin de l'événement (au format JJ/MM/AAAA)"
                + " ou 'q' pour quitter\n> "
            )
            if not ending_event_date or ending_event_date == "q":
                return None
            elif re.match(self.DATE_TYPE, ending_event_date):
                display_green_message("Le format de la date est bonne.")
            else:
                display_red_message(
                    "Le format doit être JJ/MM/AAAA"
                    + " et doit être une date cohérente."
                )
                continue
            location = self.menu.information_menu(
                asking_sentence="Veuillez remplir le lieux"
            )
            if not location:
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
            return {
                "starting_event_date": starting_event_date,
                "ending_event_date": ending_event_date,
                "location": location,
                "attendees": attendees,
                "notes": notes,
            }

    # Update method
    def update_event_informations(self, event):
        print("Vous voulez mettre à jour:\n" + str(event))
        starting_event_date = input(
            "Entrez la date de début de l'événement (au format JJ/MM/AAAA) ou 'q' pour quitter\n> "
        )
        if not starting_event_date or starting_event_date == "q":
            display_red_message("Pas de modification.")
        elif re.match(self.DATE_TYPE, starting_event_date):
            display_green_message("La date été changé.")
            event.starting_event_date = starting_event_date
        else:
            display_red_message("Le format doit être JJ/MM/AAAA.")
        ending_event_date = input(
            "Entrez la date de fin de l'événement (au format JJ/MM/AAAA)"
            + " ou 'q' pour quitter\n> "
        )
        if not ending_event_date or ending_event_date == "q":
            display_red_message("Pas de modification.")
        elif re.match(self.DATE_TYPE, ending_event_date):
            display_green_message("La date été changé.")
            event.ending_event_date = ending_event_date
        else:
            display_red_message("Le format doit être JJ/MM/AAAA.")
        location = self.menu.information_menu(
            asking_sentence="Veuillez remplir le lieux"
        )
        if not location or location == event.location:
            display_red_message("Pas de modification.")
        else:
            event.location = location
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

    # Menu to select a function
    def choice_menu(self, user_role):
        if user_role == "Manager":
            options = {
                "t": "Voir tout les événements",
                "tf": "Voir tous les événements sans affectation",
                "u": "Mettre à jour un événement",
            }
        elif user_role == "Support":
            options = {
                "t": "Voir tout les événements",
                "tf": "Voir tous les événements qui vous sont affectés",
                "u": "Mettre à jour un événement",
            }
        else:
            options = {
                "t": "Voir tout les événements",
                "a": "Créer un événement",
            }
        choice = self.menu.global_menu(options)
        return choice
