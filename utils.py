"""Define utils"""

import secrets
import string
from colorama import init, Fore, Style

# Init from colorama
init()


def display_red_message(message):
    print(f"{Fore.RED} {message} {Style.RESET_ALL}")


def display_green_message(message):
    print(f"{Fore.GREEN} {message} {Style.RESET_ALL}")


def generate_password(length=12):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = "".join(secrets.choice(alphabet) for _ in range(length))
    print(
        "Voici le password généré:\n"
        + f"{Fore.GREEN}{password}{Style.RESET_ALL}"
        + "\nPensé à bien le noté, il ne sera afficher qu'une seule fois"
        + " et il est a transmettre à votre nouveau collaborateur.\n"
        + " Il sera demander pour la première connexion."
    )
    return password


class Menu:
    """Class created to not repeat some part of code like menu structure."""

    def global_menu(self, options):
        """Create a menu in while loop,
        destinated to views, options need to be a dict.
        This function include -'q' option like other choice.
        You need to consider if 'q' option is selected out of
        this function to quit."""
        try:
            options = dict(options)
        except ValueError:
            raise ValueError(
                f"{Fore.RED}"
                + "La variable options doit être un dictionnaire."
                + f"{Style.RESET_ALL}"
            )
        choice_option = ["q"]
        while True:
            for option_name, option_description in options.items():
                print(f"{Fore.CYAN}-{option_name}: {option_description};")
                if option_name not in choice_option:
                    choice_option.append(option_name)
            print("-q: Quitter ce menu." + f"{Style.RESET_ALL}")
            choice = input("Entrez votre choix\n> ").lower()
            if choice == "":
                display_red_message("Votre choix ne peut pas être vide.")
            elif choice not in choice_option:
                display_red_message("Votre choix n'est pas compris")
            else:
                return choice

    def information_menu(
        self,
        asking_sentence,
        possible_response=None,
        value_in_sentence=None,
        not_conform_message=None,
        in_lower=False,
    ):
        """Create a menu in while loop,
        destinated to views.
        The parameter asking_sentence defines the prompt shown
        to the user for input.
        If possible_response is passed, it is used to check if choice is in possible_response.
        If value_in_sentence is passed, it is used to check
        if value_in_sentence in choice. Use not_conform_message too.
        This function include -'q' option like other choice.
        If 'q' option is selected, this method will return None"""
        choice = ""
        while choice != "q" or choice != "Q":
            try:
                asking_sentence = str(asking_sentence)
            except ValueError:
                display_red_message(
                    "La variable asking_sentence doit être une chaine de caractère"
                )
                return None
            if possible_response and value_in_sentence:
                raise TypeError(
                    "Cette méthode ne peut prendre qu'une possible_response ou une"
                    + " value_in_sentence, mais pas les deux à la fois."
                )
            if not_conform_message:
                try:
                    not_conform_message = str(not_conform_message)
                except ValueError:
                    display_red_message(
                        "La variable not_conform_message doit"
                        + " être une chaine de caractère"
                    )
            if in_lower:
                choice = input(
                    f"{asking_sentence} ou 'q' pour quitter" + "\n> "
                ).lower()
            else:
                choice = input(f"{asking_sentence} ou 'q' pour quitter" + "\n> ")
            if not choice:
                display_red_message("Ce champ ne peut pas être vide")
            elif choice == "q" or choice == "Q":
                return None
            elif possible_response:
                if choice not in possible_response and not_conform_message:
                    display_red_message(f"{not_conform_message}")
                elif choice not in possible_response and not not_conform_message:
                    display_red_message(
                        "La réponse donnée ne correspond pas aux attentes."
                    )
                else:
                    return choice
            elif value_in_sentence:
                if value_in_sentence not in choice and not_conform_message:
                    display_red_message(
                        f"{Fore.RED} {not_conform_message} {Style.RESET_ALL}"
                    )
                elif value_in_sentence not in choice and not not_conform_message:
                    display_red_message(
                        "La réponse donnée ne correspond pas aux attentes."
                    )
                else:
                    return choice
            else:
                return choice

    def confirm_choice(self, to_confirm):
        confirmation = self.information_menu(
            asking_sentence="êtes-vous sûr de vouloir supprimer "
            + f" {to_confirm} (y/n)"
        )
        if confirmation == "y":
            return True
        return False

    def crud_menu(self, designation):
        menu_options = {
            "t": f"Voir tout les {designation}s",
            "a": f"Ajoutez un {designation}",
            "u": f"Mettez à jour un {designation}",
            "d": f"Supprimez un {designation}",
        }
        menu = self.global_menu(options=menu_options)
        if menu == "q":
            return None
        return menu

    def no_permission_menu(self):
        menu_options = {
            "t": "Voir tout les contrats",
        }
        menu = self.global_menu(options=menu_options)
        if menu == "q":
            return None
        return menu
