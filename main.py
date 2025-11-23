# main.py

import sys
import os
from tkinter import messagebox

# ----------------------------------------------------------------------
# Configuración del Path y Comprobación de Importaciones
# ----------------------------------------------------------------------

# Asegura que el directorio actual esté en el PATH para importaciones locales
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.append(current_dir)
except NameError:
    pass

# Importar los componentes necesarios
try:
    # Módulos de Login
    from views.funcion_vista_login import LoginView 
    from controllers.login_controllers import LoginController 
    
    # Módulo del Menú Principal
    from views.menu import main as start_menu_app # Importamos la función 'main' de menu.py

except ImportError as e:
    error_msg = f"Error al importar un módulo requerido. Verifique que 'login_controllers.py', 'funcion_vista_login.py' y 'menu.py' existan en la misma carpeta.\nError: {e}"
    messagebox.showerror("❌ Error Crítico de Importación", error_msg)
    sys.exit(1)


# ----------------------------------------------------------------------
# Función de Orquestación
# ----------------------------------------------------------------------

def start_login_process():
    """Inicializa y ejecuta el proceso de Login."""
    
    # 1. Instanciar la Vista de Login
    login_view = LoginView(controller=None) 
    
    # 2. Instanciar el Controlador, pasándole la vista y el callback de éxito
    controller = LoginController(
        login_view=login_view, 
        success_callback=start_menu_app # El callback es la función main(role) de menu.py
    )
    
    # 3. Asignar el controlador real a la vista
    login_view.controller = controller
    
    # 4. Iniciar el bucle principal de la ventana de Login
    # Cuando el login sea exitoso, el controlador llamará a start_menu_app(role)
    login_view.mainloop() 


# ----------------------------------------------------------------------
# PUNTO DE ENTRADA PRINCIPAL
# ----------------------------------------------------------------------

if __name__ == "__main__":
    start_login_process()