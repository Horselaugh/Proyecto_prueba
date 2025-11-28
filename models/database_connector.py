# models/database_connector.py
import sqlite3
from sqlite3 import Error
import os

class Database:
    """
    Clase para manejar la conexión a la base de datos SQLite (SINGLETON)
    """
    # 1. Almacena la instancia única
    _instance = None 
    
    # 2. El método __new__ controla la creación de la instancia
    def __new__(cls):
        if cls._instance is None:
            # Crear la instancia si no existe
            cls._instance = super(Database, cls).__new__(cls)
            
            # Inicializar atributos (ejecutado solo en la primera creación)
            cls._instance.database_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "Proyecto_ultima.db"
            )
            # Aseguramos que la conexión inicie como None
            cls._instance.connection = None 
            print("[SINGLETON] Instancia de Database creada y lista.")
            
        return cls._instance
    
    def crearConexion(self):
        """Establece conexión con la base de datos SQLite"""
        try:
            # En SQLite, para reutilizar, verificamos si la conexión está viva con un simple chequeo.
            # No hay un atributo 'closed' directo. Intentamos devolver la existente.
            if self.connection:
                try:
                    # Intenta ejecutar una consulta simple para verificar si está activa
                    self.connection.execute("SELECT 1").close() 
                    print("Conexión existente reutilizada")
                    return self.connection
                except Exception:
                    # Si falla (conexión cerrada, rota, etc.), la cerramos y la re-creamos.
                    self.connection = None
            
            # Si no hay conexión o falló el chequeo, la creamos
            self.connection = sqlite3.connect(self.database_path)
            # Habilitar claves foráneas
            self.connection.execute("PRAGMA foreign_keys = ON")
            print("Conexión a la base de datos SQLite establecida")
            return self.connection
        except Error as e:
            print(f"Error conectando a la base de datos: {e}")
            self.connection = None # Asegurar que la conexión es None si falla
            return None
    
    def cerrarConexion(self, conexion=None):
        """Cierra la conexión con la base de datos"""
        connection_to_close = conexion or self.connection
        if connection_to_close:
            try:
                connection_to_close.close()
                # Restablecer la conexión del Singleton a None si cerramos la conexión principal
                if connection_to_close is self.connection: 
                     self.connection = None
                print("Conexión a la base de datos cerrada")
            except Error as e:
                 print(f"Error al cerrar la conexión: {e}")