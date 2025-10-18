# database_connector.py
import sqlite3
from sqlite3 import Error

class Database:
    
    def __init__(self, db_archivo="Proyecto_ultima.db"):
        self.db_archivo = db_archivo
        self.conexion = None
        # Verificar e inicializar la base de datos automáticamente
        self._inicializar_base_datos()

    def _inicializar_base_datos(self):
        """
        Verifica si las tablas existen y las crea si es necesario
        """
        try:
            # Primero crear una conexión temporal para verificar
            temp_conn = sqlite3.connect(self.db_archivo)
            cursor = temp_conn.cursor()
            
            # Verificar si la tabla persona existe (como indicador principal)
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='persona'")
            tabla_persona_existe = cursor.fetchone()
            
            temp_conn.close()
            
            if not tabla_persona_existe:
                print("🔄 Inicializando base de datos por primera vez...")
                self._crear_tablas()
                self._insertar_datos_catalogo()
                print("✅ Base de datos inicializada correctamente")
            else:
                print("✅ Base de datos ya está inicializada")
                
        except Error as e:
            print(f"❌ Error al verificar/inicializar base de datos: {e}")

    def _crear_tablas(self):
        """
        Crea todas las tablas del sistema
        """
        SQL_SCRIPT_CREACION = """
-- Habilitar la integridad referencial
PRAGMA foreign_keys = ON;

---------------------------------
-- TABLA BASE
---------------------------------
CREATE TABLE IF NOT EXISTS persona(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    documento_identidad TEXT UNIQUE,
    primer_nombre TEXT NOT NULL,
    segundo_nombre TEXT,
    primer_apellido TEXT NOT NULL,
    segundo_apellido TEXT,
    genero TEXT CHECK(genero IN('M', 'F')),
    direccion TEXT NOT NULL,
    telefono TEXT NOT NULL UNIQUE,
    fecha_registro DATE DEFAULT CURRENT_DATE,
    activo BOOLEAN DEFAULT TRUE
);

---------------------------------
-- TABLAS ESPECIALIZADAS (PERSONA)
---------------------------------
CREATE TABLE IF NOT EXISTS nna(
    persona_id INTEGER PRIMARY KEY,
    fecha_nacimiento DATE NOT NULL CHECK(fecha_nacimiento <= CURRENT_DATE),
    FOREIGN KEY (persona_id) REFERENCES persona(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS familiar(
    persona_id INTEGER PRIMARY KEY,
    tutor BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (persona_id) REFERENCES persona(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tercero(
    persona_id INTEGER PRIMARY KEY,
    relacion_nna TEXT CHECK (relacion_nna IN('VECINO', 'DOCENTE', 'ENTIDAD_JURIDICA', 'OTRO')),
    FOREIGN KEY (persona_id) REFERENCES persona(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS personal(
    persona_id INTEGER PRIMARY KEY,
    cargo INTEGER,
    resolucion TEXT, -- Unicamente para consejeros
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (persona_id) REFERENCES persona(id) ON DELETE CASCADE,
    FOREIGN KEY (cargo) REFERENCES cargo(id)
);

---------------------------------
-- TABLAS DE RELACIONES
---------------------------------
CREATE TABLE IF NOT EXISTS relacion_nna(
    nna_id INTEGER,
    familiar_id INTEGER,
    parentesco INTEGER,
    convive BOOLEAN DEFAULT TRUE NOT NULL,
    PRIMARY KEY (nna_id, familiar_id, parentesco),
    FOREIGN KEY (nna_id) REFERENCES nna(persona_id),
    FOREIGN KEY (familiar_id) REFERENCES familiar(persona_id),
    FOREIGN KEY (parentesco) REFERENCES parentesco(id)
);

CREATE TABLE IF NOT EXISTS unidad_educativa(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    director TEXT NOT NULL,
    tipo TEXT CHECK(tipo IN('PUBLICA', 'PRIVADA')),
    direccion TEXT NOT NULL, 
    telefono TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS matricula_educativa(
    nna_id INTEGER,
    unidad_id INTEGER,
    grado TEXT,
    fecha_matricula DATE DEFAULT CURRENT_DATE,
    activa BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (nna_id, unidad_id),
    FOREIGN KEY (nna_id) REFERENCES nna(persona_id),
    FOREIGN KEY (unidad_id) REFERENCES unidad_educativa(id)
);

CREATE TABLE IF NOT EXISTS articulos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT UNIQUE NOT NULL,
    articulo TEXT NOT NULL,
    descripcion TEXT NOT NULL
); 

CREATE TABLE IF NOT EXISTS expediente(
    nna_id INTEGER,
    articulo_id INTEGER,
    tipo TEXT CHECK(tipo IN('PROTECCION', 'TRAMITE_ADMINISTRATIVO', 'ASESORIA')) NOT NULL,
    fecha_realizacion DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (nna_id, articulo_id, tipo),
    FOREIGN KEY (nna_id) REFERENCES nna(persona_id),
    FOREIGN KEY (articulo_id) REFERENCES articulos(id)  
);

---------------------------------
-- TABLAS DE DENUNCIA
---------------------------------
CREATE TABLE IF NOT EXISTS denuncia(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    consejero_id INTEGER,
    fecha_denuncia DATE DEFAULT CURRENT_DATE,
    fecha_hechos DATE NOT NULL,
    descripcion TEXT NOT NULL,
    estado BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (consejero_id) REFERENCES personal(persona_id)
);

CREATE TABLE IF NOT EXISTS nna_involucrado(
    denuncia_id INTEGER NOT NULL,
    nna_id INTEGER NOT NULL,
    rol TEXT CHECK(rol IN('VICTIMA', 'AGRESOR', 'TESTIGO')),
    detalle_participacion TEXT,
    PRIMARY KEY (denuncia_id, nna_id),
    FOREIGN KEY (denuncia_id) REFERENCES denuncia(id),
    FOREIGN KEY (nna_id) REFERENCES nna(persona_id)
);

CREATE TABLE IF NOT EXISTS denunciante(
    denuncia_id INTEGER NOT NULL,
    persona_id INTEGER, -- Puede ser NULL si es anónimo
    declaracion TEXT NOT NULL,
    lesiones TEXT, 
    PRIMARY KEY (denuncia_id, persona_id),
    FOREIGN KEY (denuncia_id) REFERENCES denuncia(id) ON DELETE CASCADE,
    FOREIGN KEY (persona_id) REFERENCES persona(id)
);

CREATE TABLE IF NOT EXISTS denunciado(
    denuncia_id INTEGER NOT NULL,
    persona_id INTEGER NOT NULL, 
    medidas TEXT, 
    PRIMARY KEY (denuncia_id, persona_id),
    FOREIGN KEY (denuncia_id) REFERENCES denuncia(id),
    FOREIGN KEY (persona_id) REFERENCES persona(id)
);

CREATE TABLE IF NOT EXISTS seguimiento(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    denuncia_id INTEGER NOT NULL UNIQUE,
    consejero_id INTEGER NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    observaciones TEXT NOT NULL,
    FOREIGN KEY (denuncia_id) REFERENCES denuncia(id) ON DELETE CASCADE,
    FOREIGN KEY (consejero_id) REFERENCES personal(persona_id)
);

CREATE TABLE IF NOT EXISTS cierre(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    denuncia_id INTEGER NOT NULL UNIQUE,
    consejero_id INTEGER NOT NULL,
    fecha_cierre DATE DEFAULT CURRENT_DATE,
    acta_cierre TEXT NOT NULL,
    FOREIGN KEY (denuncia_id) REFERENCES denuncia(id) ON DELETE CASCADE,
    FOREIGN KEY (consejero_id) REFERENCES personal(persona_id)
);

---------------------------------
-- ENTIDADES CATALOGO
---------------------------------
CREATE TABLE IF NOT EXISTS parentesco(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT
);

CREATE TABLE IF NOT EXISTS cargo(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    requiere_resolucion BOOLEAN DEFAULT FALSE
);
"""
        conn = None
        try:
            conn = self.crearConexion()
            if conn:
                conn.executescript(SQL_SCRIPT_CREACION)
                print("✅ Tablas creadas exitosamente")
        except Error as e:
            print(f"❌ Error al crear tablas: {e}")
        finally:
            if conn:
                self.cerrarConexion()

    def _insertar_datos_catalogo(self):
        """
        Inserta datos básicos en las tablas de catálogo
        """
        conn = None
        try:
            conn = self.crearConexion()
            if not conn:
                return

            cursor = conn.cursor()
            
            # Insertar parentescos básicos
            parentescos = [
                ('Padre', 'Parentesco paterno'),
                ('Madre', 'Parentesco materno'),
                ('Hermano/a', 'Parentesco fraternal'),
                ('Tío/a', 'Parentesco de tío'),
                ('Abuelo/a', 'Parentesco de abuelo'),
                ('Primo/a', 'Parentesco de primo'),
                ('Otro', 'Otro tipo de parentesco')
            ]
            
            cursor.executemany(
                "INSERT OR IGNORE INTO parentesco (nombre, descripcion) VALUES (?, ?)",
                parentescos
            )
            
            # Insertar cargos básicos
            cargos = [
                ('Consejero', True),
                ('Coordinador', False),
                ('Psicólogo', False),
                ('Abogado', False),
                ('Asistente Social', False)
            ]
            
            cursor.executemany(
                "INSERT OR IGNORE INTO cargo (nombre, requiere_resolucion) VALUES (?, ?)",
                cargos
            )
            
            # Insertar artículos básicos
            articulos = [
                ('ART001', 'Protección Integral', 'Medidas de protección integral para NNA'),
                ('ART002', 'Derecho a la Educación', 'Garantizar el acceso a la educación'),
                ('ART003', 'Derecho a la Salud', 'Acceso a servicios de salud'),
                ('ART004', 'Protección contra Violencia', 'Protección contra toda forma de violencia')
            ]
            
            cursor.executemany(
                "INSERT OR IGNORE INTO articulos (codigo, articulo, descripcion) VALUES (?, ?, ?)",
                articulos
            )
            
            conn.commit()
            print("✅ Datos de catálogo insertados correctamente")
            
        except Error as e:
            print(f"❌ Error al insertar datos de catálogo: {e}")
        finally:
            if conn:
                self.cerrarConexion()

    # Se define la función de crear la conexión a la base de datos
    def crearConexion(self):
        try:
            self.conexion = sqlite3.connect(self.db_archivo)
            # Habilitar claves foráneas
            self.conexion.execute("PRAGMA foreign_keys = ON")
            return self.conexion
        
        except Error as e:
            print(f"❌ Error: {e}. Al tratar de conectar a la base de datos")
            return None
    
    # Se define la función que cierra la conexión con la base de datos
    def cerrarConexion(self):
        if self.conexion:
            self.conexion.close()
            self.conexion = None

# Crear una instancia global para usar en otros módulos
database = Database()