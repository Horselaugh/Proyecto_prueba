import os
import sys
import warnings 
from tkinter import messagebox

# Importamos el controlador aquí (antes de la Vista)
from controllers.login_controllers import LoginController 
from views.funcion_vista_login import LoginView 
from views.menu import main as start_menu_app # Importamos la función 'main' de menu.py


try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.append(current_dir)
except NameError:
    warnings.warn("Advertencia: No se pudo determinar el directorio actual para agregar al PATH. Las importaciones locales podrían fallar.", stacklevel=1)
    pass

# ----------------------------------------------------------------------
# Función de Orquestación (Corregida)
# ----------------------------------------------------------------------

def start_login_process():
    """Inicializa y ejecuta el proceso de Login, conectando la Vista con el Controlador."""
    
    # 1. Crear una INSTANCIA de la Vista (sin pasarle el controlador aún)
    login_view = LoginView()
    controller_instance = LoginController(
        login_view=login_view, 
        success_callback=start_menu_app
    )
    
    # 3. CONECTAR: Asignar la INSTANCIA del controlador a la vista.
    # Esto resuelve el 'AttributeError: 'function' object has no attribute 'handle_login''
    login_view.controller = controller_instance
    
    # 4. Iniciar el bucle de la interfaz gráfica
    login_view.mainloop() 


if __name__ == "__main__":
    start_login_process()