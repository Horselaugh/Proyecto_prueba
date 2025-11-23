import customtkinter as ctk
from tkinter import messagebox
import sys
import os

# 1. Configuración de path para importaciones
# Añadir el directorio padre al path para manejar importaciones relativas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 2. 🟢 CORRECCIÓN EN IMPORTACIÓN: Importar MenuApp al inicio
try:
    # Asume que 'views.menu' es el módulo correcto (debes tener views/menu.py)
    from views.menu import MenuApp 
except ImportError:
    # Definición de un Mock compatible en caso de que MenuApp no se encuentre
    class MenuApp:
        # 🟢 CORRECCIÓN: El mock ahora acepta el argumento next_module_ref
        def __init__(self, next_module_ref):
            self.next_module_ref = next_module_ref
            self.app = ctk.CTk()
            self.app.title("MenuApp Mock (Error de Importación)")
            self.app.geometry("200x100")
            ctk.CTkLabel(self.app, text="Menu Principal (Mock)").pack(pady=20)
        def mainloop(self):
            # Simplemente ejecuta el mock y destruye si se llama
            self.app.mainloop()
            self.app.destroy()
            
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class LoginApp:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("Consejo de Protección de Niños, Niñas y Adolescentes Carrizal")
        self.app.geometry("400x350")
        self.app.resizable(False, False)

        # Centrar la ventana en la pantalla
        self.center_window()

        self.frame = ctk.CTkFrame(master=self.app)
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

        self.valid_users = {
            "admin": "admin123",
            "usuario": "contraseña",
            "cpnna": "carrizal2024"
        }

    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.app.update_idletasks()
        width = self.app.winfo_width()
        height = self.app.winfo_height()
        x = (self.app.winfo_screenwidth() // 2) - (width // 2)
        y = (self.app.winfo_screenheight() // 2) - (height // 2)
        self.app.geometry(f'{width}x{height}+{x}+{y}')

    def login(self):
        usuario = self.usuario_entry.get()
        password = self.password_entry.get()

        if not usuario or not password:
            messagebox.showerror("Error", "Por favor, complete todos los campos")
            return

        # Aquí se debería llamar a un controlador o modelo para verificar credenciales
        if usuario in self.valid_users and self.valid_users[usuario] == password:
            messagebox.showinfo("Inicio exitoso", f"Bienvenido, {usuario}!")
            self.open_main_window()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
            self.password_entry.delete(0, 'end')  # Limpiar campo de contraseña

    def registro(self):
        register_window = ctk.CTkToplevel(self.app)
        register_window.title("Registro")
        register_window.geometry("400x400")
        register_window.resizable(False, False)
        register_window.transient(self.app)  # Hacerla modal
        register_window.grab_set()  # Bloquear la ventana principal

        # Centrar ventana de registro
        register_window.update_idletasks()
        width = register_window.winfo_width()
        height = register_window.winfo_height()
        x = (register_window.winfo_screenwidth() // 2) - (width // 2)
        y = (register_window.winfo_screenheight() // 2) - (height // 2)
        register_window.geometry(f'{width}x{height}+{x}+{y}')

        label = ctk.CTkLabel(register_window, text="Crear nueva cuenta", font=('Arial', 20))
        label.pack(pady=20)

        # Campos de registro
        nuevo_usuario = ctk.CTkEntry(register_window, placeholder_text="Nuevo usuario")
        nuevo_usuario.pack(pady=10, padx=20, fill='x')

        nueva_password = ctk.CTkEntry(register_window, placeholder_text="Nueva contraseña", show="*")
        nueva_password.pack(pady=10, padx=20, fill='x')

        confirmar_password = ctk.CTkEntry(register_window, placeholder_text="Confirmar contraseña", show="*")
        confirmar_password.pack(pady=10, padx=20, fill='x')

        def registrar():
            usuario = nuevo_usuario.get()
            pwd = nueva_password.get()
            confirm_pwd = confirmar_password.get()

            if not usuario or not pwd or not confirm_pwd:
                messagebox.showerror("Error", "Complete todos los campos")
                return

            if pwd != confirm_pwd:
                messagebox.showerror("Error", "Las contraseñas no coinciden")
                return

            if usuario in self.valid_users:
                messagebox.showerror("Error", "El usuario ya existe")
                return

            self.valid_users[usuario] = pwd
            messagebox.showinfo("Éxito", "Usuario registrado correctamente")
            register_window.destroy()

        btn_registrar = ctk.CTkButton(register_window, text="Registrar", command=registrar)
        btn_registrar.pack(pady=20)

    def open_main_window(self):
        """Abrir el menú principal después del login exitoso"""
        self.app.destroy()
        
        # 🟢 CORRECCIÓN CLAVE: Definir y pasar el argumento next_module_ref
        # Esta lista mutable se pasa a MenuApp para que pueda indicar 
        # al módulo de login cuál es el siguiente paso ("menu" o "exit").
        next_module_ref = ["menu"] 
        
        try:
            # 🟢 CORRECCIÓN: Pasar el argumento requerido al constructor
            main_app = MenuApp(next_module_ref) 
            main_app.mainloop()
            
            # Opcional: Si MenuApp modificó next_module_ref, actuar en consecuencia
            if next_module_ref[0] == "exit":
                sys.exit(0)
                
        except Exception as e:
             # Manejar cualquier otro error que pueda ocurrir al iniciar MenuApp
            messagebox.showerror("Error Crítico", f"No se pudo iniciar el menú principal: {str(e)}")
            sys.exit(1)


    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    app = LoginApp()
    app.run()