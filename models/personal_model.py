# models/personal_model.py
import sys
import os
import sqlite3
from sqlite3 import Error, IntegrityError
from typing import List, Dict, Optional

# Agregar el directorio actual al path para importar database_connector
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from database_connector import Database
except ImportError:
    # Simulación de la clase Database si no está disponible para pruebas
    class Database:
        def crearConexion(self): return None
        def cerrarConexion(self, conexion): pass
    # Importar el módulo real si está disponible
    from models.database_connector import Database

class PersonalModel:
    """Modelo para gestionar las operaciones de Personal en la base de datos"""

    def __init__(self):
        self.db = Database()
        
    def _mapear_personal(self, fila: dict) -> dict:
        """Función interna para mapear una fila de la BD a un diccionario.
           Añadidos campos faltantes de persona y usuario.
        """
        if not fila:
            return None
        return {
            "persona_id": fila["id"],
            "documento_identidad": fila["documento_identidad"],
            "primer_nombre": fila["primer_nombre"],
            "segundo_nombre": fila.get("segundo_nombre"), # Añadido
            "primer_apellido": fila["primer_apellido"],
            "segundo_apellido": fila.get("segundo_apellido"), # Añadido
            "telefono": fila["telefono"],
            "direccion": fila.get("direccion"), # Añadido
            "genero": fila.get("genero"), # Código de género (M/F/O)
            "cargo": fila["cargo"],
            "resolucion": fila["resolucion"],
            "nombre_usuario": fila.get("nombre_usuario"), # Añadido (desde tabla 'usuario')
            "activo": bool(fila["activo"])
        }

    def agregar_personal(self, datos: dict) -> int:
        """Inserta un nuevo registro en Persona, Personal y Usuario dentro de una transacción."""
        
        sql_persona = """
        INSERT INTO persona (documento_identidad, primer_nombre, segundo_nombre, 
                             primer_apellido, segundo_apellido, telefono, direccion, genero, activo) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, TRUE)
        """
        
        sql_personal = """
        INSERT INTO personal (persona_id, cargo, resolucion, activo) 
        VALUES (?, ?, ?, TRUE)
        """
        
        # Asumimos una tabla 'usuario' para credenciales de acceso
        sql_usuario = """
        INSERT INTO usuario (persona_id, nombre_usuario, password_hash)
        VALUES (?, ?, ?)
        """
        
        conexion = self.db.crearConexion()
        if conexion is None:
            raise Error("No se pudo establecer conexión con la base de datos.")

        try:
            cursor = conexion.cursor()
            
            # 1. Ejecutar INSERT en persona
            cursor.execute(sql_persona, (
                datos["cedula"], datos["primer_nombre"], datos.get("segundo_nombre"),
                datos["primer_apellido"], datos.get("segundo_apellido"), 
                datos["telefono"], datos.get("direccion", "N/A"), datos.get("genero", "M")
            ))
            persona_id = cursor.lastrowid
            
            # 2. Ejecutar INSERT en personal
            cursor.execute(sql_personal, (
                persona_id, 
                datos.get("cargo"), 
                datos.get("resolucion")
            ))
            
            # 3. Ejecutar INSERT en usuario (el controlador debe enviar el hash de la contraseña)
            password_hash = datos.get("password")
            if not password_hash:
                 raise ValueError("La contraseña hasheada es requerida para el registro de usuario.")

            cursor.execute(sql_usuario, (
                persona_id,
                datos.get("nombre_usuario"),
                password_hash
            ))

            conexion.commit()
            return persona_id

        except IntegrityError as e:
            conexion.rollback()
            raise IntegrityError(f"Error de integridad. El registro ya existe. {e}")
        except Error as e:
            conexion.rollback()
            raise Error(f"Error de BD al registrar personal: {e}")
        finally:
            if conexion:
                self.db.cerrarConexion(conexion)

    def obtener_por_id(self, persona_id: int) -> Optional[dict]:
        """Busca un registro de Personal por su ID, incluyendo todos los campos y el usuario."""
        sql = """
        SELECT 
            p.id, p.documento_identidad, p.primer_nombre, p.segundo_nombre, p.primer_apellido, 
            p.segundo_apellido, p.telefono, p.direccion, p.genero,
            pe.cargo, pe.resolucion, p.activo,
            u.nombre_usuario 
        FROM persona p
        INNER JOIN personal pe ON p.id = pe.persona_id
        LEFT JOIN usuario u ON p.id = u.persona_id
        WHERE p.id = ?;
        """
        conexion = self.db.crearConexion()
        if conexion is None:
            return None

        try:
            conexion.row_factory = sqlite3.Row
            cursor = conexion.cursor()
            cursor.execute(sql, (persona_id,))
            fila = cursor.fetchone()
            return self._mapear_personal(dict(fila)) if fila else None
        except Error as e:
            print(f"Error al obtener personal por ID: {e}")
            return None
        finally:
            if conexion:
                self.db.cerrarConexion(conexion)
                
    def obtener_por_cedula(self, documento_identidad: str) -> Optional[dict]:
        """Busca un registro de Personal por su Cédula/Documento de Identidad, incluyendo todos los campos y el usuario."""
        sql = """
        SELECT 
            p.id, p.documento_identidad, p.primer_nombre, p.segundo_nombre, p.primer_apellido, 
            p.segundo_apellido, p.telefono, p.direccion, p.genero,
            pe.cargo, pe.resolucion, p.activo,
            u.nombre_usuario 
        FROM persona p
        INNER JOIN personal pe ON p.id = pe.persona_id
        LEFT JOIN usuario u ON p.id = u.persona_id
        WHERE p.documento_identidad = ?;
        """
        conexion = self.db.crearConexion()
        if conexion is None:
            return None

        try:
            conexion.row_factory = sqlite3.Row
            cursor = conexion.cursor()
            cursor.execute(sql, (documento_identidad,))
            fila = cursor.fetchone()
            return self._mapear_personal(dict(fila)) if fila else None
        except Error as e:
            print(f"Error al obtener personal por Cédula: {e}")
            return None
        finally:
            if conexion:
                self.db.cerrarConexion(conexion)

    def listar_todo(self) -> List[dict]:
        """Lista todos los registros de Personal activos, incluyendo todos los campos y el usuario."""
        sql = """
        SELECT 
            p.id, p.documento_identidad, p.primer_nombre, p.segundo_nombre, p.primer_apellido, 
            p.segundo_apellido, p.telefono, p.direccion, p.genero,
            pe.cargo, pe.resolucion, p.activo,
            u.nombre_usuario 
        FROM persona p
        INNER JOIN personal pe ON p.id = pe.persona_id
        LEFT JOIN usuario u ON p.id = u.persona_id 
        WHERE p.activo = TRUE;
        """
        conexion = self.db.crearConexion()
        if conexion is None:
            return []

        try:
            conexion.row_factory = sqlite3.Row
            cursor = conexion.cursor()
            cursor.execute(sql)
            filas = cursor.fetchall()
            return [self._mapear_personal(dict(fila)) for fila in filas]
        except Error as e:
            print(f"Error al listar personal: {e}")
            return []
        finally:
            if conexion:
                self.db.cerrarConexion(conexion)

    def actualizar_personal(self, datos: dict) -> bool:
        """Actualiza los datos del Personal en Persona, Personal y Usuario (opcionalmente la contraseña)."""
        
        if 'persona_id' not in datos:
            return False
            
        sql_persona = """
        UPDATE persona SET 
            documento_identidad = ?, primer_nombre = ?, segundo_nombre = ?, primer_apellido = ?, 
            segundo_apellido = ?, telefono = ?, direccion = ?, genero = ?
        WHERE id = ?;
        """
        
        sql_personal = """
        UPDATE personal SET 
            cargo = ?, resolucion = ?
        WHERE persona_id = ?;
        """
        
        # 💡 Actualizar nombre de usuario
        sql_usuario = """
        UPDATE usuario SET 
            nombre_usuario = ?
        WHERE persona_id = ?;
        """
        
        # 💡 Actualizar hash de la contraseña (solo si se provee uno nuevo)
        sql_password_update = """
        UPDATE usuario SET 
            password_hash = ?
        WHERE persona_id = ?;
        """
        
        conexion = self.db.crearConexion()
        if conexion is None:
            raise Error("No se pudo establecer conexión para actualizar.")

        try:
            cursor = conexion.cursor()
            
            # 1. Actualizar Persona (ahora incluye segundo_nombre, segundo_apellido, direccion, genero)
            cursor.execute(sql_persona, (
                datos.get("cedula"), datos.get("primer_nombre"), datos.get("segundo_nombre"),
                datos.get("primer_apellido"), datos.get("segundo_apellido"), 
                datos.get("telefono"), datos.get("direccion"), datos.get("genero"), 
                datos["persona_id"]
            ))
            
            # 2. Actualizar Personal
            cursor.execute(sql_personal, (
                datos.get("cargo"), datos.get("resolucion"), datos["persona_id"]
            ))
            
            # 3. Actualizar Usuario
            cursor.execute(sql_usuario, (
                datos.get("nombre_usuario"), datos["persona_id"]
            ))
            
            # 4. Actualizar Contraseña (Opcional)
            password_hash = datos.get("password")
            if password_hash: 
                cursor.execute(sql_password_update, (
                    password_hash, datos["persona_id"]
                ))
            
            conexion.commit()
            return True 

        except IntegrityError as e:
            conexion.rollback()
            raise IntegrityError(f"Error de integridad al actualizar (documento o usuario duplicado). {e}")
        except Error as e:
            conexion.rollback()
            raise Error(f"Error de BD al actualizar personal: {e}")
        finally:
            if conexion:
                self.db.cerrarConexion(conexion)

    def eliminar_personal(self, persona_id: int) -> bool:
        """Realiza un borrado lógico estableciendo el campo 'activo' a FALSE en la tabla persona."""
        
        sql = "UPDATE persona SET activo = FALSE WHERE id = ?;"
        
        conexion = self.db.crearConexion()
        if conexion is None:
            raise Error("No se pudo establecer conexión para la eliminación.")

        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (persona_id,))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as e:
            raise Error(f"Error de BD al eliminar personal: {e}")
        finally:
            if conexion:
                self.db.cerrarConexion(conexion)

    def obtener_por_usuario(self, nombre_usuario: str) -> Optional[dict]:
        """Busca un registro de Personal por el nombre de usuario (útil para login)."""
        return None
    
    def listar_cargos(self) -> List[dict]:
        """Lista todos los registros de cargos disponibles."""
        sql = "SELECT id, nombre, requiere_resolucion FROM cargo ORDER BY nombre;"
        
        conexion = self.db.crearConexion()
        if conexion is None:
            return []

        try:
            conexion.row_factory = sqlite3.Row
            cursor = conexion.cursor()
            cursor.execute(sql)
            filas = cursor.fetchall()
            # Mapear las filas a un diccionario simple para el controlador
            return [dict(fila) for fila in filas]
        except Error as e:
            print(f"Error al listar cargos: {e}")
            return []
        finally:
            if conexion:
                self.db.cerrarConexion(conexion)