import customtkinter as ctk
from tkinter import messagebox
import sys
import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# ----------------------------------------------------------------------
# CLASE VISTA (LoginView)
# ----------------------------------------------------------------------

class LoginView(ctk.CTk):
    """La interfaz gráfica de la ventana de Login, que interactúa con LoginController."""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller 
        self.title("Inicio de Sesión")
        self.geometry("400x350")
        self.resizable(False, False)
        self.center_window()

        self.frame = ctk.CTkFrame(master=self) 
        self.frame.pack(pady=20, padx=40, fill='both', expand=True)

        self.label = ctk.CTkLabel(master=self.frame, text='Inicio de Sesión', font=('Arial', 24))
        self.label.pack(pady=12, padx=10)

        self.usuario_entry = ctk.CTkEntry(master=self.frame, placeholder_text="Usuario")
        self.usuario_entry.pack(pady=12, padx=10)

        self.password_entry = ctk.CTkEntry(master=self.frame, placeholder_text="Contraseña", show="*")
        self.password_entry.pack(pady=12, padx=10)

        # Bind Enter key to login
        self.usuario_entry.bind("<Return>", lambda e: self.login())
        self.password_entry.bind("<Return>", lambda e: self.login())

        self.remember = ctk.CTkCheckBox(master=self.frame, text="Recordar usuario")
        self.remember.pack(pady=12, padx=10)

        self.button = ctk.CTkButton(master=self.frame, text='Iniciar Sesión', command=self.login)
        self.button.pack(pady=12, padx=10)

        self.register_label = ctk.CTkLabel(master=self.frame, text="Regístrate", cursor="hand2", 
                                         text_color="#1f6aa5")
        self.register_label.pack(pady=12, padx=10)
        self.register_label.bind("<Button-1>", lambda e: self.registro())
        
    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')


    def login(self):
        """Llama al controlador para procesar el login."""
        usuario = self.usuario_entry.get()
        password = self.password_entry.get()

        if not usuario or not password:
            messagebox.showerror("Error", "Por favor, complete todos los campos")
            return

        # Pasa la responsabilidad al controlador (incluyendo la limpieza y el cierre)
        self.controller.handle_login(usuario, password) 
        
        # NOTA: La limpieza de la contraseña se movió al controlador para evitar el TclError.
        

    def registro(self):
        # Implementación completa de la ventana de registro
        register_window = ctk.CTkToplevel(self) 
        register_window.title("Registro")
        register_window.geometry("400x400")
        register_window.resizable(False, False)
        register_window.transient(self) 
        register_window.grab_set()

        # Componentes de la UI de registro
        frame = ctk.CTkFrame(master=register_window)
        frame.pack(pady=20, padx=40, fill='both', expand=True)

        label = ctk.CTkLabel(master=frame, text='Registro de Nuevo Usuario', font=('Arial', 18))
        label.pack(pady=12, padx=10)

        reg_usuario_entry = ctk.CTkEntry(master=frame, placeholder_text="Nuevo Usuario")
        reg_usuario_entry.pack(pady=12, padx=10)

        reg_password_entry = ctk.CTkEntry(master=frame, placeholder_text="Contraseña", show="*")
        reg_password_entry.pack(pady=12, padx=10)

        reg_password_confirm_entry = ctk.CTkEntry(master=frame, placeholder_text="Confirmar Contraseña", show="*")
        reg_password_confirm_entry.pack(pady=12, padx=10)

        def registrar():
            """Lógica de validación y llamada al controlador para registro."""
            usuario = reg_usuario_entry.get()
            password = reg_password_entry.get()
            password_confirm = reg_password_confirm_entry.get()
            
            if not usuario or not password or not password_confirm:
                messagebox.showerror("Error de Registro", "Por favor, complete todos los campos.", parent=register_window)
                return

            if password != password_confirm:
                messagebox.showerror("Error de Registro", "Las contraseñas no coinciden.", parent=register_window)
                return
            
            # Llama al controlador para registrar el usuario
            if self.controller.handle_registration(usuario, password):
                messagebox.showinfo("Éxito", f"Usuario '{usuario}' registrado correctamente.", parent=register_window)
                register_window.destroy()
            else:
                messagebox.showerror("Error de Registro", f"El usuario '{usuario}' ya existe o hubo un error al guardar.", parent=register_window)


        register_button = ctk.CTkButton(master=frame, text='Registrar', command=registrar)
        register_button.pack(pady=20, padx=10)

# ----------------------------------------------------------------------
# PUNTO DE ENTRADA DE PRUEBA INDEPENDIENTE (IGNORAR ESTE BLOQUE AL USAR main.py)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     ...