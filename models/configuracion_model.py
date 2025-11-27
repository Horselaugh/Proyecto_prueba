import sqlite3
import sys
import os
import random
from sqlite3 import Row
from typing import List, Dict, Optional

# Añadir el path para que las importaciones relativas funcionen
sys.path.append(os.path.join(os.path.dirname(__file__)))

# 🚨 CAMBIO CLAVE: Importar directamente la clase Database desde database_connector
# Se asume que database_connector.py está en la misma carpeta o accesible por path.
try:
    from database_connector import Database  # Usamos la clase Database (Singleton)
except ImportError:
    # Esto manejaría el caso si la estructura de carpetas es diferente (models/database_connector)
    # y la importación del nivel superior falla.
    print("Advertencia: No se pudo importar Database directamente. Intentando models.database_connector...")
    from models.database_connector import Database


class ConfiguracionModel:
    """
    Modelo que maneja las operaciones de configuración del sistema
    """
    
    def __init__(self):
        # 🚨 CAMBIO CLAVE: Inicializar self.db con la instancia Singleton de Database
        # La clase Database del archivo database_connector.py actúa como un Singleton.
        self.db = Database()
        self._inicializar_base_datos()
    
    def _inicializar_base_datos(self) -> bool:
        """Inicializa la base de datos con las tablas necesarias"""
        # 🚨 CAMBIO CLAVE: Usar obtener_conexion/cerrar_conexion de la clase Database
        # NOTA: La clase Database en database_connector.py no tiene `obtener_conexion` ni 
        # `cerrar_conexion` en el código proporcionado. Solo tiene `crearConexion` y 
        # `cerrarConexion`. Asumo que se desea usar el método `crearConexion` 
        # y que se ha modificado la clase `Database` para tener `obtener_conexion` o 
        # que `crearConexion` se usará en su lugar.
        
        # Basado en el uso previo de database_connector.py, asumiremos que los métodos son:
        # obtener_conexion -> crearConexion
        # cerrar_conexion -> cerrarConexion
        conn = self.db.crearConexion() # Usando crearConexion en lugar de obtener_conexion
        if conn is None:
            return False
        
        try:
            cursor = conn.cursor()
            
            # Tabla persona
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS persona(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    documento_identidad TEXT UNIQUE,
                    primer_nombre TEXT NOT NULL,
                    segundo_nombre TEXT,
                    primer_apellido TEXT NOT NULL,
                    segundo_apellido TEXT,
                    genero TEXT CHECK(genero IN('M', 'F')), 
                    direccion TEXT NOT NULL,
                    telefono TEXT UNIQUE,
                    fecha_registro DATE DEFAULT CURRENT_DATE
                );
            """)
            
            # Tabla rol
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rol(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL UNIQUE,
                    descripcion TEXT
                );
            """)

            # Tabla persona_rol
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS persona_rol(
                    persona_id INTEGER NOT NULL,
                    rol_id INTEGER NOT NULL,
                    fecha_asignacion DATE DEFAULT CURRENT_DATE,
                    PRIMARY KEY (persona_id, rol_id),
                    FOREIGN KEY (persona_id) 
                        REFERENCES persona(id) ON DELETE CASCADE,
                    FOREIGN KEY (rol_id) 
                        REFERENCES rol(id) ON DELETE CASCADE
                );
            """)
            
            # Tabla cargo
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cargo(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL,
                    descripcion TEXT,
                    requiere_resolucion BOOLEAN DEFAULT FALSE
                );
            """)
            
            # Insertar cargo por defecto
            cursor.execute(
                "INSERT OR IGNORE INTO cargo (id, nombre) VALUES (1, 'AdministradorTemporal')"
            )

            # Tabla personal
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS personal(
                    persona_id INTEGER NOT NULL,
                    cargo_id INTEGER NOT NULL,
                    resolucion TEXT UNIQUE NOT NULL,
                    fecha_ingreso DATE NOT NULL,
                    fecha_egreso DATE,
                    activo BOOLEAN DEFAULT TRUE, 
                    nombre_usuario TEXT UNIQUE NOT NULL,
                    contraseña TEXT NOT NULL,
                    PRIMARY KEY (persona_id, cargo_id),
                    FOREIGN KEY (persona_id) 
                        REFERENCES persona(id) ON DELETE CASCADE,
                    FOREIGN KEY (cargo_id) 
                        REFERENCES cargo(id) ON DELETE CASCADE
                );
            """)
            
            # Insertar rol por defecto
            try:
                cursor.execute(
                    "INSERT OR IGNORE INTO rol (nombre, descripcion) VALUES (?, ?)", 
                    ('Administrador', 'Rol administrativo del sistema')
                )
            except sqlite3.IntegrityError:
                pass  # Ya existe, no hacer nada
            
            conn.commit()
            return True
            
        except sqlite3.Error as e:
            print(f"Error al inicializar la base de datos: {e}")
            return False
        finally:
            self.db.cerrarConexion(conn) # Usando cerrarConexion
    
    # --- Operaciones de Roles ---
    
    def obtener_todos_los_roles(self) -> List[Row]:
        """Obtiene todos los roles de la base de datos"""
        query = "SELECT id, nombre, descripcion FROM rol ORDER BY nombre"
        
        try:
            conn = self.db.crearConexion() # Usando crearConexion
            if conn is None:
                return []
                
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
            
        except sqlite3.Error as e:
            print(f"Error al obtener roles: {e}")
            return []
        finally:
            self.db.cerrarConexion(conn) # Usando cerrarConexion
    
    def insertar_rol(self, nombre: str, descripcion: str = "") -> Optional[int]:
        """Inserta un nuevo rol y retorna su ID"""
        query = "INSERT INTO rol (nombre, descripcion) VALUES (?, ?)"
        
        try:
            conn = self.db.crearConexion() # Usando crearConexion
            if conn is None:
                return None
                
            cursor = conn.cursor()
            cursor.execute(query, (nombre, descripcion))
            conn.commit()
            return cursor.lastrowid
            
        except sqlite3.IntegrityError as e:
            print(f"Error de integridad: El rol {nombre} ya existe. {e}")
            return None
        except sqlite3.Error as e:
            print(f"Error al insertar rol {nombre}: {e}")
            return None
        finally:
            self.db.cerrarConexion(conn) # Usando cerrarConexion
    
    def modificar_rol(self, rol_id: int, nuevo_nombre: str, 
                      nueva_descripcion: str = "") -> bool:
        """Modifica un rol existente"""
        query = "UPDATE rol SET nombre = ?, descripcion = ? WHERE id = ?"
        
        try:
            conn = self.db.crearConexion() # Usando crearConexion
            if conn is None:
                return False
                
            cursor = conn.cursor()
            cursor.execute(query, (nuevo_nombre, nueva_descripcion, rol_id))
            conn.commit()
            return cursor.rowcount > 0
            
        except sqlite3.IntegrityError as e:
            print(f"Error de integridad: El rol {nuevo_nombre} ya existe. {e}")
            return False
        except sqlite3.Error as e:
            print(f"Error al modificar rol ID {rol_id}: {e}")
            return False
        finally:
            self.db.cerrarConexion(conn) # Usando cerrarConexion
    
    def eliminar_rol(self, rol_id: int) -> bool:
        """Elimina un rol de la base de datos"""
        query = "DELETE FROM rol WHERE id = ?"
        
        try:
            conn = self.db.crearConexion() # Usando crearConexion
            if conn is None:
                return False
                
            cursor = conn.cursor()
            cursor.execute(query, (rol_id,))
            conn.commit()
            return cursor.rowcount > 0
            
        except sqlite3.Error as e:
            print(f"Error al eliminar rol ID {rol_id}: {e}")
            return False
        finally:
            self.db.cerrarConexion(conn) # Usando cerrarConexion
    
    # --- Operaciones de Usuarios ---
    
    def obtener_todos_los_usuarios(self) -> List[Row]:
        """Obtiene todos los usuarios con sus datos completos"""
        query = """
            SELECT 
                per.id as persona_id,
                per.primer_nombre as nombre_usuario,
                per.primer_apellido,
                per.segundo_apellido,
                per.documento_identidad,
                per.direccion,
                per.telefono,
                r.nombre as rol_nombre,
                r.id as rol_id
            FROM personal p
            JOIN persona per ON p.persona_id = per.id
            LEFT JOIN persona_rol pr ON p.persona_id = pr.persona_id
            LEFT JOIN rol r ON pr.rol_id = r.id
            ORDER BY per.primer_nombre, per.primer_apellido
        """
        
        try:
            conn = self.db.crearConexion() # Usando crearConexion
            if conn is None:
                return []
                
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
            
        except sqlite3.Error as e:
            print(f"Error al obtener usuarios: {e}")
            return []
        finally:
            self.db.cerrarConexion(conn) # Usando cerrarConexion
    
    def insertar_usuario(self, datos_usuario: Dict) -> Optional[int]:
        """Inserta un nuevo usuario y retorna el ID de persona"""
        conn = self.db.crearConexion() # Usando crearConexion
        if conn is None:
            return None
        
        try:
            cursor = conn.cursor()
            
            # Generar datos únicos
            telefono_unico = f'555-{random.randint(1000, 9999)}'
            resolucion_num = (
                f"R-{datos_usuario['documento_identidad']}"
                f"-{random.randint(10, 99)}"
            )
            
            # 1. Insertar en tabla persona
            cursor.execute("""
                INSERT INTO persona (
                    primer_nombre, segundo_nombre, primer_apellido, 
                    segundo_apellido, documento_identidad, genero, 
                    direccion, telefono
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                datos_usuario['primer_nombre'],
                datos_usuario.get('segundo_nombre'),
                datos_usuario['primer_apellido'],
                datos_usuario.get('segundo_apellido'),
                datos_usuario['documento_identidad'],
                datos_usuario.get('genero', 'F'),
                datos_usuario['direccion'],
                telefono_unico
            ))
            
            persona_id = cursor.lastrowid
            
            # 2. Insertar en tabla personal
            cursor.execute("""
                INSERT INTO personal (
                    persona_id, cargo_id, resolucion, fecha_ingreso, 
                    nombre_usuario, contraseña
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                persona_id,
                1,  # cargo_id temporal
                resolucion_num,
                datos_usuario.get('fecha_ingreso', '2025-01-01'),
                datos_usuario['primer_nombre'],  # nombre_usuario
                datos_usuario.get('contraseña', 'password')  # contraseña por defecto
            ))
            
            # 3. Asignar rol si se especifica
            if datos_usuario.get('rol_id'):
                cursor.execute("""
                    INSERT INTO persona_rol (persona_id, rol_id) VALUES (?, ?)
                """, (persona_id, datos_usuario['rol_id']))
            
            conn.commit()
            return persona_id
            
        except sqlite3.IntegrityError as e:
            conn.rollback()
            if "UNIQUE constraint failed: persona.documento_identidad" in str(e):
                raise ValueError("El Documento de Identidad ya existe") from e
            if "UNIQUE constraint failed: personal.nombre_usuario" in str(e):
                raise ValueError(
                    f"El nombre de usuario '{datos_usuario['primer_nombre']}' ya existe"
                ) from e
            raise ValueError(f"Error de unicidad: {e}") from e
        except sqlite3.Error as e:
            conn.rollback()
            raise Exception(f"Error al insertar usuario: {e}") from e
        finally:
            self.db.cerrarConexion(conn) # Usando cerrarConexion
    
    def modificar_usuario(self, datos_usuario: Dict) -> bool:
        """Modifica un usuario existente"""
        conn = self.db.crearConexion() # Usando crearConexion
        if conn is None:
            return False
        
        try:
            cursor = conn.cursor()
            
            # 1. Actualizar datos en tabla persona
            cursor.execute("""
                UPDATE persona SET 
                    primer_nombre = ?,
                    segundo_nombre = ?,
                    primer_apellido = ?,
                    segundo_apellido = ?,
                    documento_identidad = ?,
                    direccion = ?
                WHERE id = ?
            """, (
                datos_usuario['primer_nombre'],
                datos_usuario.get('segundo_nombre'),
                datos_usuario['primer_apellido'],
                datos_usuario.get('segundo_apellido'),
                datos_usuario['documento_identidad'],
                datos_usuario['direccion'],
                datos_usuario['persona_id']
            ))
            
            # 2. Actualizar nombre de usuario si cambió
            if (datos_usuario.get('nombre_usuario_anterior') != 
                    datos_usuario['primer_nombre']):
                cursor.execute("""
                    UPDATE personal SET nombre_usuario = ? WHERE persona_id = ?
                """, (datos_usuario['primer_nombre'], datos_usuario['persona_id']))
            
            # 3. Actualizar rol
            if datos_usuario.get('rol_id'):
                cursor.execute(
                    "DELETE FROM persona_rol WHERE persona_id = ?", 
                    (datos_usuario['persona_id'],)
                )
                cursor.execute(
                    "INSERT INTO persona_rol (persona_id, rol_id) VALUES (?, ?)", 
                    (datos_usuario['persona_id'], datos_usuario['rol_id'])
                )
            
            conn.commit()
            return True
            
        except sqlite3.IntegrityError as e:
            conn.rollback()
            if "UNIQUE constraint failed: persona.documento_identidad" in str(e):
                raise ValueError("El Documento de Identidad ya existe") from e
            if "UNIQUE constraint failed: personal.nombre_usuario" in str(e):
                raise ValueError("El nuevo nombre de usuario ya existe") from e
            raise ValueError(f"Error de unicidad: {e}") from e
        except sqlite3.Error as e:
            conn.rollback()
            raise Exception(f"Error al modificar usuario: {e}") from e
        finally:
            self.db.cerrarConexion(conn) # Usando cerrarConexion
    
    def eliminar_usuario(self, persona_id: int) -> bool:
        """Elimina un usuario de la base de datos"""
        query = "DELETE FROM persona WHERE id = ?"
        
        try:
            conn = self.db.crearConexion() # Usando crearConexion
            if conn is None:
                return False
                
            cursor = conn.cursor()
            cursor.execute(query, (persona_id,))
            conn.commit()
            return cursor.rowcount > 0
            
        except sqlite3.Error as e:
            print(f"Error al eliminar usuario ID {persona_id}: {e}")
            return False
        finally:
            self.db.cerrarConexion(conn) # Usando cerrarConexion