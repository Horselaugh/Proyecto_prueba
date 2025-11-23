from models.login_models import UserModel
from views.funcion_vista_login import LoginView 
import tkinter.messagebox as msg

class LoginController:
    """
    Controlador encargado de la lógica de validación de usuario 
    y de orquestar el inicio del menú principal tras un login exitoso.
    """
    def __init__(self, login_view, success_callback):
        self.model = UserModel()
        self.view = login_view
        self.success_callback = success_callback # Función que inicia MenuApp (start_menu_app)

    def handle_login(self, username, password):
        """Maneja el intento de login."""
        
        # 1. Validar con el Modelo
        role = self.model.validate_user(username, password)
        
        if role:
            msg.showinfo("Acceso concedido", f"Bienvenido {username}. Rol: {role}")
            
            # CORRECCIÓN para evitar TclError: Limpiar el campo ANTES de llamar a self.view.quit()
            self.view.password_entry.delete(0, 'end') 
            
            # 2. Detiene el bucle principal de la ventana de login
            self.view.quit()     
            
            # 3. Ejecuta el callback para iniciar MenuApp, pasando el rol
            self.success_callback(role) 
        else:
            msg.showerror("Error", "Usuario o contraseña incorrectos")

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