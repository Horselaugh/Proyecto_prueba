# base_de_datos/db_initializer.py

from database_connector import Database
from sqlite3 import Error

# Script SQL que contiene todas las sentencias CREATE TABLE
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
    -- El campo anonimo es redundante en SQLite, la clave es manejar persona_id como NULL
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

def crear_tablas():
    """
    Crea todas las tablas de la base de datos definidas en el script SQL.
    Utiliza el gestor de conexión (Database) para obtener la conexión.
    """
    db = Database()
    conexion = db.obtener_conexion()
    
    if conexion is None:
        print("Error: No se pudo establecer conexión para crear las tablas.")
        return False
    
    try:
        with conexion:
            # Usamos executescript para ejecutar múltiples sentencias SQL
            conexion.executescript(SQL_SCRIPT_CREACION)
            print("✔️ Todas las tablas del sistema han sido creadas exitosamente.")
            return True
            
    except Error as e:
        print(f"❌ Ha ocurrido un error mientras se estaban creando las tablas: {str(e)}")
        return False

# Ejemplo de uso (opcional)
if __name__ == '__main__':
    crear_tablas()