import os
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from db import Database


class LoginGUI:
    def __init__(self, root, db):
        self.root = root
        self.root.title("Login")
        screen_width = 1024
        screen_height = 768
        root.geometry(f"{screen_width}x{screen_height}")

        # Set the appearance mode and theme
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        # Set the window icon
        self.icon_image = tk.PhotoImage(file=os.path.join(os.getcwd(), "images/admin_icon.png"))
        self.root.iconphoto(False, self.icon_image)

        # Background image
        self.bg_image = Image.open(os.path.join(os.getcwd(), "images/main_background.jpg"))
        self.bg_image = self.bg_image.resize((screen_width, screen_height), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Second background image
        self.second_bg_image = Image.open(os.path.join(os.getcwd(), "images/background_2.jpg"))
        self.second_bg_image = self.second_bg_image.resize((500, 500), Image.LANCZOS)
        self.second_bg_photo = ImageTk.PhotoImage(self.second_bg_image)

        initial_x = screen_width
        initial_y = screen_height // 3

        self.my_canvas = tk.Canvas(root, width=initial_x, height=screen_height)
        self.my_canvas.pack(fill="both", expand=True)
        self.my_canvas.create_image(0, 0, image=self.bg_photo, anchor='nw')
        self.my_canvas.create_image((initial_x // 2) - 500 / 2, (screen_height // 2) - 500 / 2, image=self.second_bg_photo, anchor='nw')

        self.my_canvas.create_text((initial_x // 2), (screen_height // 4), text="Admin Login", font=("Montserrat", 40, "bold"), fill="black")

        # Username field
        username_frame = tk.Frame(self.my_canvas)
        self.my_canvas.create_text((initial_x // 3), initial_y, text="Username", font=("Ariel", 20, "bold"), fill="black")
        self.entry_username = ctk.CTkEntry(username_frame, corner_radius=50, bg_color="white", width=420, height=35, border_color="black")
        self.entry_username.grid()
        self.my_canvas.create_window((initial_x // 3.5), initial_y + 30, anchor="nw", window=username_frame)

        # Password field
        password_frame = tk.Frame(self.my_canvas)
        self.my_canvas.create_text((initial_x // 3), initial_y + 120, text="Password", font=("Ariel", 20, "bold"), fill="black")
        self.entry_password = ctk.CTkEntry(password_frame, show="*", corner_radius=50, bg_color="white", width=420, height=35, border_color="black")
        self.entry_password.grid()
        self.my_canvas.create_window((initial_x // 3.5), initial_y + 150, anchor="nw", window=password_frame)

        # Toggle password visibility button
        self.button_toggle_password = ctk.CTkButton(self.root, text="Show", corner_radius=0, width=75, height=35, border_width=1, border_color="black", command=self.toggle_password)
        self.my_canvas.create_window(initial_x // 1.60, initial_y + 150, anchor="nw", window=self.button_toggle_password)

        # Login button
        button_frame = tk.Frame(self.my_canvas)
        self.button_login = ctk.CTkButton(button_frame, text="Log In", corner_radius=10, bg_color="white", font=("Segoe UI", 20, "bold"), command=self.authenticate)
        self.button_login.grid(ipadx=140)
        self.button_login.grid(ipady=2)
        self.my_canvas.create_window((initial_x // 3.5), initial_y + 240, anchor="nw", window=button_frame)

        # Create Account button
        create_button_frame = tk.Frame(self.my_canvas)
        self.button_create_account = ctk.CTkButton(create_button_frame, text="Create Account", corner_radius=10, bg_color="white",text_color="black", font=("Segoe UI", 15, "bold"), command=self.go_to_create_account)
        self.button_create_account.grid(ipadx=10)
        self.button_create_account.grid(ipady=1)
        self.my_canvas.create_window((initial_x // 1.85), initial_y + 280, anchor="nw", window=create_button_frame)

        # Error label
        self.error_label = self.my_canvas.create_text((initial_x // 2), initial_y + 325, text="", font=("Segoe UI", 16, "bold"))

        # Initialize the database
        self.db = db

    def toggle_password(self):
        """Toggle the visibility of the password."""
        if self.entry_password.cget('show') == '*':
            self.entry_password.configure(show='')
            self.button_toggle_password.configure(text="Hide")
        else:
            self.entry_password.configure(show='*')
            self.button_toggle_password.configure(text="Show")

    def authenticate(self):
        """Authenticate the user using the database."""
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        # Check if fields are empty
        if not username or not password:
            self.my_canvas.itemconfig(self.error_label, text="Username and Password cannot be empty.", fill="red")
            return

        # Authenticate using the database
        if self.db.authenticate_user(username, password):
            self.my_canvas.itemconfig(self.error_label, text="Login Successful!!!", fill="green")
            self.root.after(1000, self.go_to_dashboard)
        else:
            self.my_canvas.itemconfig(self.error_label, text="Incorrect Username or Password", fill="red")

    def go_to_create_account(self):
        """Destroy the login window and open the Create Account screen."""
        self.root.destroy()
        self.open_create_account()

    def open_create_account(self):
        """Initialize the Create Account window."""
        create_account_root = ctk.CTk()
        CreateAccount(create_account_root, self.db)
        create_account_root.mainloop()

    def go_to_dashboard(self):
        """Destroy the login window and open the dashboard."""
        self.root.destroy()
        main_dashboard()

    def __del__(self):
        """Ensure the database connection is closed when the object is destroyed."""
        self.db.close()

class CreateAccount:
    def __init__(self, root, db):
        self.db = db
        self.root = root
        self.root.title("Create Account")
        screen_width = 1024
        screen_height = 768
        root.geometry(f"{screen_width}x{screen_height}")

        # Set the appearance mode and theme
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        # Set the window icon
        self.icon_image = tk.PhotoImage(file=os.path.join(os.getcwd(), "images/admin_icon.png"))
        self.root.iconphoto(False, self.icon_image)

        # Background image
        self.bg_image = Image.open(os.path.join(os.getcwd(), "images/main_background.jpg"))
        self.bg_image = self.bg_image.resize((screen_width, screen_height), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Second background image
        self.second_bg_image = Image.open(os.path.join(os.getcwd(), "images/background_2.jpg"))
        self.second_bg_image = self.second_bg_image.resize((500, 500), Image.LANCZOS)
        self.second_bg_photo = ImageTk.PhotoImage(self.second_bg_image)

        initial_x = screen_width
        initial_y = screen_height // 3

        self.my_canvas = tk.Canvas(root, width=initial_x, height=screen_height)
        self.my_canvas.pack(fill="both", expand=True)
        self.my_canvas.create_image(0, 0, image=self.bg_photo, anchor='nw')
        self.my_canvas.create_image((initial_x // 2) - 500 / 2, (screen_height // 2) - 500 / 2, image=self.second_bg_photo, anchor='nw')

        self.my_canvas.create_text((initial_x // 2), (screen_height // 4), text="Create Account", font=("Montserrat", 40, "bold"), fill="black")

        # Username field
        username_frame = tk.Frame(self.my_canvas)
        self.my_canvas.create_text((initial_x // 3), initial_y, text="Username", font=("Ariel", 20, "bold"), fill="black")
        self.entry_username = ctk.CTkEntry(username_frame, corner_radius=50, bg_color="white", width=420, height=35, border_color="black")
        self.entry_username.grid()
        self.my_canvas.create_window((initial_x // 3.5), initial_y + 30, anchor="nw", window=username_frame)

        # Password field
        password_frame = tk.Frame(self.my_canvas)
        self.my_canvas.create_text((initial_x // 3), initial_y + 120, text="Password", font=("Ariel", 20, "bold"), fill="black")
        self.entry_password = ctk.CTkEntry(password_frame, show="*", corner_radius=50, bg_color="white", width=420, height=35, border_color="black")
        self.entry_password.grid()
        self.my_canvas.create_window((initial_x // 3.5), initial_y + 150, anchor="nw", window=password_frame)

        # Toggle password visibility button
        self.button_toggle_password = ctk.CTkButton(self.root, text="Show", corner_radius=0, width=75, height=35, border_width=1, border_color="black", command=self.toggle_password)
        self.my_canvas.create_window(initial_x // 1.60, initial_y + 150, anchor="nw", window=self.button_toggle_password)

        button_frame = tk.Frame(self.my_canvas)
        self.button_create_account = ctk.CTkButton(button_frame, text="Create Account", corner_radius=10, bg_color="white", font=("Segoe UI", 20, "bold"), command=self.create_account)
        self.button_create_account.grid(ipadx=130)
        self.button_create_account.grid(ipady=2)
        self.my_canvas.create_window((initial_x // 3.5), initial_y + 240, anchor="nw", window=button_frame)

        # Create Account button
        create_button_frame = tk.Frame(self.my_canvas)
        self.button_create_account = ctk.CTkButton(create_button_frame, text="Login", corner_radius=10, bg_color="white",text_color="black", font=("Segoe UI", 15, "bold"), command=self.go_to_login_page)
        self.button_create_account.grid(ipadx=10)
        self.button_create_account.grid(ipady=1)
        self.my_canvas.create_window((initial_x // 1.83), initial_y + 280, anchor="nw", window=create_button_frame)

        self.error_label = self.my_canvas.create_text((initial_x // 2), initial_y + 310, text="", font=("Segoe UI", 16, "bold"))


    def toggle_password(self):
        """Toggle the visibility of the password."""
        if self.entry_password.cget('show') == '*':
            self.entry_password.configure(show='')
            self.button_toggle_password.configure(text="Hide")
        else:
            self.entry_password.configure(show='*')
            self.button_toggle_password.configure(text="Show")

    def create_account(self):
        """Create a new account in the database."""
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        # Check if fields are empty
        if not username or not password:
            self.my_canvas.itemconfig(self.error_label, text="Username and Password cannot be empty.", fill="red")
            return

        # Check if the user already exists
        if self.db.authenticate_user(username, password):
            self.my_canvas.itemconfig(self.error_label, text="User already exists.", fill="red")
            return

        if self.db.add_user(username, password):
            self.my_canvas.itemconfig(self.error_label, text="Account Created Successfully!", fill="green")
        else:
            self.my_canvas.itemconfig(self.error_label, text=f"Error Creating your account", fill="red")

    def go_to_login_page(self):
        """Destroy the login window and open the Create Account screen."""
        self.root.destroy()
        self.open_login_page()

    def open_login_page(self):
        """Initialize the Create Account window."""
        login_account_root = ctk.CTk()
        LoginGUI(login_account_root, self.db)
        login_account_root.mainloop()

    def __del__(self):
        """Ensure the database connection is closed when the object is destroyed."""
        self.db.close()


def main_dashboard():
    """Function to initialize the admin dashboard after login."""
    input()
    dashboard_root = ctk.CTk()
    dashboard_root.mainloop()


if __name__ == "__main__":
    root_ = ctk.CTk()
    database = Database()
    app = LoginGUI(root_, database)
    root_.mainloop()

