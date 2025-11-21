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
            cls._instance.connection = None
            print("[SINGLETON] Instancia de Database creada y lista.")
            
        return cls._instance
    
    def crearConexion(self):
        """Establece conexión con la base de datos SQLite"""
        # ... (código existente, no requiere cambios)
        try:
            # Si ya hay una conexión, la retornamos. Opcional para evitar reconexión.
            if self.connection and not self.connection.closed:
                print("Conexión existente reutilizada")
                return self.connection
                
            self.connection = sqlite3.connect(self.database_path)
            print("Conexión a la base de datos SQLite establecida")
            return self.connection
        except Error as e:
            print(f"Error conectando a la base de datos: {e}")
            return None
    
    def cerrarConexion(self, conexion=None):
        """Cierra la conexión con la base de datos"""
        # ... (código existente, no requiere cambios)
        connection_to_close = conexion or self.connection
        if connection_to_close:
            connection_to_close.close()
            # Opcionalmente, restablecer la conexión del Singleton a None
            if connection_to_close is self.connection:
                 self.connection = None
            print("Conexión a la base de datos cerrada")