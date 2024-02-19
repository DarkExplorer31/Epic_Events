"""Define utils"""

import secrets
import string
from colorama import init, Fore, Style


class Utils:
    """Class created to not repeat some part of code like menu structure."""

    def __init__(self):
        init()

    def display_red_message(self, message):
        print(f"{Fore.RED} {message} {Style.RESET_ALL}")

    def display_green_message(self, message):
        print(f"{Fore.GREEN} {message} {Style.RESET_ALL}")

    def create_menu(self, options):
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
                self.display_red_message("Votre choix ne peut pas être vide.")
            elif choice not in choice_option:
                self.display_red_message("Votre choix n'est pas compris")
            else:
                return choice

    def information_menu(
        self,
        asking_sentence,
        constant=None,
        reverse_constant=None,
        not_in_constant_message=None,
        in_lower=False,
    ):
        """Create a menu in while loop,
        destinated to views.
        The parameter asking_sentence defines the prompt shown
        to the user for input.
        If constant is passed, it is used to check if choice is in constant.
        If reverse_constant is passed, it is used to check
        if reverse_constant in choice. Use not_in_constant_message too.
        This function include -'q' option like other choice.
        If 'q' option is selected, this method will return None"""
        choice = ""
        while choice != "q" or choice != "Q":
            try:
                asking_sentence = str(asking_sentence)
            except ValueError:
                self.display_red_message(
                    "La variable asking_sentence doit être une chaine de caractère"
                )
                return None
            if constant and reverse_constant:
                raise TypeError(
                    "Cette méthode ne peut prendre qu'une constante ou une"
                    + " constante renversé, mais pas les deux à la fois."
                )
            if not_in_constant_message:
                try:
                    not_in_constant_message = str(not_in_constant_message)
                except ValueError:
                    self.display_red_message(
                        "La variable not_in_constant_message doit"
                        + " être une chaine de caractère"
                    )
            if in_lower:
                choice = input(
                    f"{asking_sentence} ou 'q' pour quitter" + "\n> "
                ).lower()
            else:
                choice = input(f"{asking_sentence} ou 'q' pour quitter" + "\n> ")
            if not choice:
                self.display_red_message("Ce champ ne peut pas être vide")
            elif choice == "q" or choice == "Q":
                return None
            elif constant:
                if choice not in constant and not_in_constant_message:
                    self.display_red_message(f"{not_in_constant_message}")
                elif choice not in constant and not not_in_constant_message:
                    self.display_red_message(
                        "La réponse donnée ne correspond pas aux attentes."
                    )
                else:
                    return choice
            elif reverse_constant:
                if reverse_constant not in choice and not_in_constant_message:
                    self.display_red_message(
                        f"{Fore.RED} {not_in_constant_message} {Style.RESET_ALL}"
                    )
                elif reverse_constant not in choice and not not_in_constant_message:
                    self.display_red_message(
                        "La réponse donnée ne correspond pas aux attentes."
                    )
                else:
                    return choice
            else:
                return choice

    def generate_password(self, length=12):
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
