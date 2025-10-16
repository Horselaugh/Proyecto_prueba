from funcion_conexion_personal import Database
from sqlite3 import Error

class PersonalModel:

    def __init__(self):
        self.db = Database()
        self.conexion = self.db.crearConexion()
        if self.conexion:
            self.cursor = self.conexion.cursor()
        else:
            raise Exception("No se pudo conectar a la base de datos")

    def agregar_personal(self, cedula, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, telefono, nombre_usuario, password):
        if not self.conexion:
            print("No hay conexión a la base de datos")
            return None

        try:
            # Primero insertar en la tabla persona
            self.cursor.execute("""
                INSERT INTO persona (
                    documento_identidad, primer_nombre, segundo_nombre, 
                    primer_apellido, segundo_apellido, telefono, direccion
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (cedula, primer_nombre, segundo_nombre, primer_apellido, 
                 segundo_apellido, telefono, 'Por definir')  # Dirección temporal
            )
            persona_id = self.cursor.lastrowid
            
            # Luego insertar en la tabla personal
            self.cursor.execute("""
                INSERT INTO personal (persona_id, cargo, nombre_usuario, password) 
                VALUES (?, ?, ?, ?)
                """,
                (persona_id, 1, nombre_usuario, password)  # cargo=1 temporal
            )
            
            self.conexion.commit()
            return persona_id

        except Error as e:
            print(f"Error al agregar nuevo personal: {e}")
            return None