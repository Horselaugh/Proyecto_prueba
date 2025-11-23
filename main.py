import sys
import os

def setup_path():
    """
    Asegura que el directorio del proyecto y el directorio padre estén en sys.path 
    para importaciones absolutas resilientes, como 'views.funcion_login'.
    """
    # 1. Directorio que contiene este script (directorio actual)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.append(current_dir)
        
    # 2. Directorio padre (probablemente la raíz real del proyecto)
    # Al incluir el padre, se permite la importación de paquetes hermanos (ej. views/)
    project_root = os.path.dirname(current_dir)
    if project_root not in sys.path:
        sys.path.append(project_root)

# Llamar a la configuración del path al inicio
setup_path()

# Importar la clase LoginApp que contiene la lógica completa y la función run().
try:
    # Si 'views' y 'funcion_login' están configurados correctamente, la importación funciona.
    from views.funcion_login import LoginApp
except ImportError as e:
    # Este error ahora es más probable que se deba a que 'views/' o 'funcion_login.py' no existen
    # en la estructura de carpetas esperada.
    print(f"❌ Error de importación: No se pudo encontrar views.funcion_login.LoginApp.")
    print(f"Asegúrese de que el archivo 'funcion_login.py' esté en la carpeta 'views/' y no tenga errores de sintaxis.")
    print(f"Detalle del error: {e}")
    sys.exit(1)


def main():
    """Función principal para inicializar y ejecutar la aplicación de Login."""
    
    try:
        app_runner = LoginApp()
        print("Iniciando aplicación de Login...")
        app_runner.run() # Llama a self.app.mainloop() o el método de ejecución de la app
    except Exception as e:
        # Esto capturará errores que ocurran DENTRO del constructor o la función run().
        print(f"❌ Ocurrió un error al iniciar la aplicación principal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()