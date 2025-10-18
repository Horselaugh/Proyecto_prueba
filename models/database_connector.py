# models/database_connector.py
import sqlite3
from sqlite3 import Error
import os

class Database:
    """
    Clase para manejar la conexión a la base de datos SQLite
    """
    
    def __init__(self):
        self.database_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lopnna_db.sqlite")
        self.connection = None
    
    def crearConexion(self):
        """Establece conexión con la base de datos SQLite"""
        try:
            self.connection = sqlite3.connect(self.database_path)
            print("✅ Conexión a la base de datos SQLite establecida")
            return self.connection
        except Error as e:
            print(f"❌ Error conectando a la base de datos: {e}")
            return None
    
    def cerrarConexion(self, conexion=None):
        """Cierra la conexión con la base de datos"""
        connection_to_close = conexion or self.connection
        if connection_to_close:
            connection_to_close.close()
            print("✅ Conexión a la base de datos cerrada")