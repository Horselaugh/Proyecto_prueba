# tercero_model.py

from database_connector import database
from sqlite3 import Error

class TerceroModel:
    """
    Modelo para gestionar la información de terceros (Vecinos, Docentes, Entidades, etc.).
    Utiliza las tablas persona y tercero.
    """
    
    def __init__(self):
        self.db = database

    def crear_tercero(self, datos_persona, relacion_nna):
        """
        Crea un nuevo registro en la tabla persona y luego en la tabla tercero.
        Retorna el ID de la persona insertada o None si hay error.
        
        datos_persona debe ser un diccionario con las claves de la tabla persona:
        (documento_identidad, primer_nombre, segundo_nombre, primer_apellido, 
        segundo_apellido, genero, direccion, telefono)
        """
        conn = self.db.crearConexion()
        if conn is None:
            return None, "Error de conexión a la base de datos."
        
        try:
            cursor = conn.cursor()
            
            # 1. Insertar en la tabla persona
            persona_sql = """
                INSERT INTO persona (documento_identidad, primer_nombre, segundo_nombre, 
                                     primer_apellido, segundo_apellido, genero, 
                                     direccion, telefono)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """
            persona_data = (
                datos_persona['documento_identidad'], datos_persona['primer_nombre'], 
                datos_persona.get('segundo_nombre'), datos_persona['primer_apellido'], 
                datos_persona.get('segundo_apellido'), datos_persona['genero'], 
                datos_persona['direccion'], datos_persona['telefono']
            )
            cursor.execute(persona_sql, persona_data)
            persona_id = cursor.lastrowid

            # 2. Insertar en la tabla tercero
            tercero_sql = """
                INSERT INTO tercero (persona_id, relacion_nna)
                VALUES (?, ?);
            """
            cursor.execute(tercero_sql, (persona_id, relacion_nna))
            
            conn.commit()
            return persona_id, "Tercero registrado exitosamente."
        
        except Error as e:
            conn.rollback()
            print(f"[ERROR_TERCERO] Error al crear tercero: {e}")
            return None, f"Error al crear tercero: {e}"
        finally:
            self.db.cerrarConexion()

    def obtener_terceros(self):
        """
        Recupera una lista de todos los terceros registrados con sus datos de persona.
        """
        sql = """
            SELECT 
                p.id, p.documento_identidad, 
                p.primer_nombre, p.primer_apellido, 
                t.relacion_nna, p.telefono, p.direccion
            FROM persona p
            JOIN tercero t ON p.id = t.persona_id;
        """
        conn = self.db.crearConexion()
        if conn is None:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            
            columnas = [desc[0] for desc in cursor.description]
            terceros = [dict(zip(columnas, row)) for row in cursor.fetchall()]
            return terceros
        except Error as e:
            print(f"[ERROR_TERCERO] Error al obtener terceros: {e}")
            return []
        finally:
            self.db.cerrarConexion()