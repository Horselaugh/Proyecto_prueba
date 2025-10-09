import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class LoginApp:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("Consejo de Protección de Niños, Niñas y Adolescentes Carrizal")
        self.app.geometry("400x350")

        self.frame = ctk.CTkFrame(master=self.app)
        self.frame.pack(pady=20, padx=40, fill='both', expand=True)

        self.label = ctk.CTkLabel(master=self.frame, text='Inicio', font=('Arial', 24))
        self.label.pack(pady=12, padx=10)

        self.usuario_entry = ctk.CTkEntry(master=self.frame, placeholder_text="Usuario")
        self.usuario_entry.pack(pady=12, padx=10)

        self.password_entry = ctk.CTkEntry(master=self.frame, placeholder_text="Contraseña", show="*")
        self.password_entry.pack(pady=12, padx=10)

        self.remember = ctk.CTkCheckBox(master=self.frame, text="Recordar usuario")
        self.remember.pack(pady=12, padx=10)

        self.button = ctk.CTkButton(master=self.frame, text='Inicio', command=self.login)
        self.button.pack(pady=12, padx=10)

        self.register_label = ctk.CTkLabel(master=self.frame, text="Regístrate")
        self.register_label.pack(pady=12, padx=10)
        self.register_label.bind("<Button-1>", lambda e: self.registro())

        self.valid_users = {
            "admin": "admin123",
            "usuario": "contraseña"
        }

    def login(self):
        usuario = self.usuario_entry.get()
        password = self.password_entry.get()

        if usuario in self.valid_users and self.valid_users[usuario] == password:
            messagebox.showinfo("Inicio exitoso", f"Bienvenido, {usuario}!")
            self.open_main_window()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def registro(self):
        register_window = ctk.CTkToplevel(self.app)
        register_window.title("Registro")
        register_window.geometry("400x400")

        label = ctk.CTkLabel(register_window, text="Crear nueva cuenta", font=('Arial', 20))
        label.pack(pady=20)

    def open_main_window(self):
        self.app.destroy()

        main_app = ctk.CTk()
        main_app.title("Consejo de Protección de Niños, Niñas y Adolescentes Carrizal")
        main_app.geometry("800x600")

        main_app.mainloop()

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    app = LoginApp()
    app.run()