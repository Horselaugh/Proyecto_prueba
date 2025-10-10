import sqlite3
from sqlite3 import Error

class Database:
    """
    Crea la base de datos del sistema
    1. Se obtiene la conexión de la base de datos
    2. Se crean las entidades de la base de datos si estas no existen
    """
    def __init__(self, db_nombre="Proyecto_ultima.db"):
        self.db_nombre = db_nombre
        self.crear_tablas()
    
    def obtener_conexion(self) -> sqlite3.Connection:
        """Retorna una conexión activa a la base de datos"""
        try:
            return sqlite3.connect(self.db_nombre)
        except Error as e:
            print(f"No se pudo conectar con la base de datos: {str(e)}")
            return None
    # Fin de obtener_conexion
            
    def crear_tablas(self):
        """Crea las tablas de la base de datos si no existen"""
        conexion = self.obtener_conexion()
        if conexion is None:
            return False
        
        try:
            with conexion:
                cursor = conexion.cursor()
                
                # Para asegurar la integridad referencial
                cursor.execute("PRAGMA foreign_keys = ON;")
                
                # Sentencia SQL para crear TODAS las tablas:
                sql_script="""
                ---------------------------------
                -- TABLAS LOPNNA (LEGISLACIÓN) --
                ---------------------------------
                
                CREATE TABLE IF NOT EXISTS titulo(
                    id INTEGER PRIMARY KEY,
                    nombre TEXT NOT NULL UNIQUE
                );
                
                CREATE TABLE IF NOT EXISTS capitulo(
                    id INTEGER PRIMARY KEY,
                    titulo_id INTEGER NOT NULL,
                    nombre TEXT NOT NULL,
                    FOREIGN KEY (titulo_id) REFERENCES titulo(id) ON DELETE CASCADE,
                    UNIQUE (titulo_id, nombre)
                );
                
                CREATE TABLE IF NOT EXISTS articulo(
                    id INTEGER PRIMARY KEY,
                    capitulo_id INTEGER NOT NULL,
                    numero_articulo TEXT NOT NULL,
                    descripcion TEXT NOT NULL,
                    texto TEXT NOT NULL,
                    FOREIGN KEY (capitulo_id) REFERENCES capitulo(id) ON DELETE CASCADE,
                    UNIQUE (capitulo_id, numero_articulo)
                );
                 
                CREATE TABLE IF NOT EXISTS literal(
                    id INTEGER PRIMARY KEY,
                    articulo_id INTEGER NOT NULL,
                    literal_codigo TEXT NOT NULL,
                    texto TEXT NOT NULL,
                    FOREIGN KEY (articulo_id) REFERENCES articulo(id) ON DELETE CASCADE,
                    UNIQUE (articulo_id , literal_codigo)
                );
            
                """
                # Se ejecutan todas las sentencias SQL
                cursor.executescript(sql_script)
                conexion.commit()
                print("Todas las tablas del módulo expediente han sido creadas")
        except Error as e:
            print(f"Ha ocurrido un error mientras se estaban creando las tablas: {str(e)}")
            return False
    # Fin de crear_tablas