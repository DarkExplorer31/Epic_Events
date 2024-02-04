"""Authentication view"""

from tkinter import *


class AuthenticationView:
    def __init__(self):
        self.window = Tk()

    def create_window(self):
        """Method to initialize all elements of authentication window"""
        self.window.title("Epic Events Authentication")
        self.window.geometry("600x300")
        self.window.minsize(400, 400)
        self.window.configure(background="#96c0eb")
        # Add specifics elements: Username
        username_label = Label(
            self.window, text="Entrez votre identifiant:", font=("Ink free", 25)
        )
        username_label.pack()
        username_entry = Entry(self.window, font=("Courrier", 25))
        username_entry.pack()
        # Add specifics elements: Password
        password_label = Label(
            self.window, text="Entrez votre mot de passe:", font=("Ink free", 25)
        )
        password_label.pack()
        password_entry = Entry(self.window, font=("Courrier", 25))
        password_entry.pack()

    def run(self):
        self.window.mainloop()


auth_view = AuthenticationView()
auth_view.create_window()
auth_view.run()
