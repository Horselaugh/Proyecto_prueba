import customtkinter as ctk

class LoginView(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Login Profesional")
        self.geometry("400x300")

        self.label = ctk.CTkLabel(self, text="Iniciar sesión", font=("Arial", 20))
        self.label.pack(pady=10)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Usuario")
        self.username_entry.pack(pady=5)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*")
        self.password_entry.pack(pady=5)

        self.login_button = ctk.CTkButton(self, text="Entrar", command=self.login)
        self.login_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.controller.handle_login(username, password)
