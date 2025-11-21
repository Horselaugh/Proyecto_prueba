# C:\Users\Dylan\Desktop\Proyecto_prueba\main.py

import sys
import os

def setup_path():
    """Asegura que el directorio del proyecto esté en sys.path para importaciones absolutas."""
    # Agrega la carpeta raíz del proyecto al path
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.append(project_root)

# Llamar a la configuración del path al inicio
setup_path()

# Importar la clase LoginApp que contiene la lógica completa y la función run().
# NOTA: Asumiendo que 'funcion_login.py' está dentro de la carpeta 'views'.
try:
    from views.funcion_login import LoginApp
except ImportError as e:
    print(f"Error de importación: No se pudo encontrar views.funcion_login.LoginApp. Asegúrese de que el archivo esté en views/ y no haya errores de sintaxis.")
    print(f"Detalle del error: {e}")
    sys.exit(1)


def main():
    """Función principal para inicializar y ejecutar la aplicación de Login."""
    
    # **IMPORTANTE**: Llamamos a LoginApp, que no requiere el argumento 'controller'.
    try:
        app_runner = LoginApp()
        print("Iniciando aplicación de Login...")
        app_runner.run() # Llama a self.app.mainloop()
    except Exception as e:
        # Esto capturará errores que ocurran DENTRO del constructor o la función run().
        print(f"Ocurrió un error al iniciar la aplicación principal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()