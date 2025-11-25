# controllers/login_controllers.py

# Asegúrate de que esta importación exista para que el controlador pueda interactuar con la vista.
from views.funcion_vista_login import LoginView 
# Asumiendo que el modelo se usa para la lógica de negocio/base de datos
# from models.login_model import LoginModel 
from tkinter import messagebox 

class LoginController:
    """Controlador que maneja la lógica de negocio para la ventana de Login."""

    # El constructor debe aceptar los argumentos pasados desde main.py
    def __init__(self, login_view, success_callback):
        self.login_view = login_view  # Guardamos la instancia de la Vista
        self.success_callback = success_callback  # Guardamos la función a llamar tras el éxito
        # self.model = LoginModel() # Si usas un modelo

    def handle_login(self, usuario, password):
        """Procesa la solicitud de inicio de sesión."""
        
        # 1. Lógica de autenticación (Ejemplo: llamar al Modelo)
        # role = self.model.authenticate(usuario, password)
        role = "admin" # Sustituir con lógica real
        
        if role:
            messagebox.showinfo("Éxito", f"Bienvenido, {usuario} ({role}).")
            
            # 2. Cerrar la ventana de Login
            self.login_view.destroy()
            
            # 3. Llamar a la función de menú principal con el rol
            self.success_callback(role)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    # MÉTODO AÑADIDO para manejar el registro
    def handle_registration(self, username, password, role="user"):
        """Maneja el intento de registro, usa el Modelo para añadir el usuario."""
        if self.model.users.get(username):
            return False # Usuario ya existe
        
        try:
            self.model.add_user(username, password, role)
            return True
        except Exception as e:
            # En una aplicación real, se manejaría un error de base de datos aquí.
            print(f"Error al registrar usuario: {e}") 
            return False