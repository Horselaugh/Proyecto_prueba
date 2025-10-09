from db_connection import crearConexion
from sqlite3 import Error

class PersonalModel:

    def __init__(self):
        self.db = Database()
        self.conexion = self.db.crearConexion()
        if conexion:
            self.cursor = self.conexion.cursor()
        else:
            raise Exception("No se pudo conectar a la base de datos")

    def crear_tabla(self):
        if not self.conexion:
            print("No hay conexión a la base de datos")
            return False
        
        try:
            self.cursor.execute("""
                CREATE IF NOT EXISTS personal(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cedula TEXT(8) UNIQUE NOT NULL,
                    primer_nombre TEXT NOT NULL,
                    segundo_nombre TEXT,
                    primer_apellido TEXT NOT NULL,
                    segundo_apellido TEXT,
                    telefono TEXT(11) UNIQUE NOT NULL,

                    -- Configurar los siguientes atributos a futuro:
                    nombre_usuario TEXT UNIQUE NOT NULL,
                    password TEXT 
                )
            """
            )
            self.conexion.commit()

        except Error as e:
            print(f"No se ha podido crear la tabla 'personal': {e}")
            return False
        
    def generar_personal(self, cedula, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, telefono, nombre_usuario, password):
        if not self.conexion:
            print("No hay conexión a la base de datos")
            return False

        try:
            self.cursor.execute("""
                INSERT INTO personal (cedula, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, telefono, nombre_usuario, password) VALUES (NULL, ?, ?, ?, ?, ?, ?)
                ) """,
                (cedula, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, telefono, nombre_usuario, password)
            )
            self.conexion.commit()
            self.cursor.lastrowid

        except Error as e:
            print(f"Error al agregar nuevo personal: {e}")
            return None