"""User view"""


class UserView:
    def ask_authentication(self):
        login = ""
        password = ""
        while login not in ["q", "Q"] or password not in ["q", "Q"]:
            print("Bienvenue dans le menu d'authentification\n")
            login = input(
                "Veuillez entrer votre identifiant ou tappez 'q' pour sortir:\n> "
            )
            if not login:
                print("Votre login ne peut pas être vide")
                continue
            elif login in ["q", "Q"]:
                break
            password = input("Veuillez entrer votre mot de passe:\n> ")
            if not password:
                print("Votre mot de passe ne peut pas être vide")
                continue
            elif password in ["q", "Q"]:
                break
            authentication_data = [login, password]
            return authentication_data

    def display_message(self, message):
        print(message)
