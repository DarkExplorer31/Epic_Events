"""Authentication view"""

from tkinter import *


class AuthenticationView:
    def __init__(self):
        self.window = Tk()

    def toggle_password_visibility(self, password_entry, visibility_button):
        current_state = password_entry["show"]
        new_state = "" if current_state == "*" else "*"
        password_entry.config(show=new_state)
        visibility_button["text"] = "Hide PW" if new_state == "" else "See PW"

    def send_data(self, username, password):
        print("Username:", username)
        print("Password:", password)

    def create_window(self):
        """Method to initialize all elements of authentication window"""
        self.window.title("Epic Events Authentication")
        self.window.geometry("1000x200")
        self.window.maxsize(1000, 200)
        self.window.minsize(400, 400)
        self.window.configure(background="#224466")

        # Add specifics elements: Title
        title = Label(
            self.window,
            text="Epic Events",
            font=("Franklin Gothic Medium", 45),
            bg="#224466",
            fg="white",
        )
        title.grid(row=0, column=0, pady=10)

        # Add specifics elements: Username
        username_label = Label(
            self.window,
            text="Entrez votre identifiant:",
            font=("Franklin Gothic Medium", 25),
            bg="#224466",
            fg="white",
        )
        username_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        username_entry = Entry(self.window, font=("Franklin Gothic Medium", 25))
        username_entry.grid(row=1, column=1, padx=10, pady=10, sticky="e")

        # Add specifics elements: Password
        password_label = Label(
            self.window,
            text="Entrez votre mot de passe:",
            font=("Franklin Gothic Medium", 25),
            bg="#224466",
            fg="white",
        )
        password_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        password_entry = Entry(
            self.window,
            font=("Franklin Gothic Medium", 25),
            show="*",
        )
        password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="e")
        password_visibility = Button(
            self.window,
            text="See PW",
            command=lambda: self.toggle_password_visibility(
                password_entry, password_visibility
            ),
        )
        password_visibility.grid(row=2, column=2, padx=10, pady=10, sticky="w")

        # Add specifics elements: Confirm button
        confirm_button = Button(
            self.window,
            text="Confirm",
            command=lambda: self.send_data(username_entry.get(), password_entry.get()),
        )
        confirm_button.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Add specifics elements: Errors
        display_errors = Entry(self.window, state="disabled")
        display_errors.grid(row=4, column=1, padx=10, pady=10, sticky="w")

    def run(self):
        self.window.mainloop()


auth_view = AuthenticationView()
auth_view.create_window()
auth_view.run()