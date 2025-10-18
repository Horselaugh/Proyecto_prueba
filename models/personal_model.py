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
    from models.database_connector import Database

class PersonalModel:
    """Modelo para gestionar las operaciones de Personal en la base de datos"""

    def __init__(self):
        self.db = Database()
        
    def _mapear_personal(self, fila: dict) -> dict:
        """Función interna para mapear una fila de la BD a un diccionario."""
        if not fila:
            return None
        return {
            "persona_id": fila["id"],
            "documento_identidad": fila["documento_identidad"],
            "primer_nombre": fila["primer_nombre"],
            "primer_apellido": fila["primer_apellido"],
            "telefono": fila["telefono"],
            "nombre_usuario": fila["nombre_usuario"],
            "cargo": fila["cargo"],
            "resolucion": fila["resolucion"],
            "activo": bool(fila["activo"])
        }

    def agregar_personal(self, datos: dict) -> int:
        """Inserta un nuevo registro en Persona y Personal dentro de una transacción."""
        
        sql_persona = """
        INSERT INTO persona (documento_identidad, primer_nombre, segundo_nombre, 
                             primer_apellido, segundo_apellido, telefono, direccion, genero, activo) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, TRUE)
        """
        
        sql_personal = """
        INSERT INTO personal (persona_id, cargo, resolucion, activo) 
        VALUES (?, ?, ?, TRUE)
        """
        
        conexion = self.db.crearConexion()
        if conexion is None:
            raise Error("No se pudo establecer conexión con la base de datos.")

        try:
            cursor = conexion.cursor()
            
            # Ejecutar INSERT en persona
            cursor.execute(sql_persona, (
                datos["cedula"], datos["primer_nombre"], datos.get("segundo_nombre"),
                datos["primer_apellido"], datos.get("segundo_apellido"), 
                datos["telefono"], datos.get("direccion", "N/A"), datos.get("genero", "M")
            ))
            persona_id = cursor.lastrowid
            
            # Ejecutar INSERT en personal
            cursor.execute(sql_personal, (
                persona_id, 
                datos.get("cargo"), 
                datos.get("resolucion")
            ))
            
            conexion.commit()
            return persona_id

        except IntegrityError as e:
            raise IntegrityError(f"Error de integridad. El registro ya existe. {e}")
        except Error as e:
            raise Error(f"Error de BD al registrar personal: {e}")
        finally:
            if conexion:
                self.db.cerrarConexion(conexion)

    def obtener_por_id(self, persona_id: int) -> Optional[dict]:
        """Busca un registro de Personal por su ID."""
        sql = """
        SELECT 
            p.id, p.documento_identidad, p.primer_nombre, p.primer_apellido, 
            p.telefono, pe.cargo, pe.resolucion, p.activo
        FROM persona p
        INNER JOIN personal pe ON p.id = pe.persona_id
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
            return dict(fila) if fila else None
        except Error as e:
            print(f"Error al obtener personal por ID: {e}")
            return None
        finally:
            if conexion:
                self.db.cerrarConexion(conexion)

    def listar_todo(self) -> List[dict]:
        """Lista todos los registros de Personal activos."""
        sql = """
        SELECT 
            p.id, p.documento_identidad, p.primer_nombre, p.primer_apellido, 
            p.telefono, pe.cargo, pe.resolucion, p.activo
        FROM persona p
        INNER JOIN personal pe ON p.id = pe.persona_id
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
            return [dict(fila) for fila in filas]
        except Error as e:
            print(f"Error al listar personal: {e}")
            return []
        finally:
            if conexion:
                self.db.cerrarConexion(conexion)

    def actualizar_personal(self, datos: dict) -> bool:
        """Actualiza los datos del Personal en ambas tablas."""
        
        if 'persona_id' not in datos:
            return False
            
        sql_persona = """
        UPDATE persona SET 
            documento_identidad = ?, primer_nombre = ?, primer_apellido = ?, 
            telefono = ?, direccion = ?, genero = ?
        WHERE id = ?;
        """
        
        sql_personal = """
        UPDATE personal SET 
            cargo = ?, resolucion = ?
        WHERE persona_id = ?;
        """
        
        conexion = self.db.crearConexion()
        if conexion is None:
            raise Error("No se pudo establecer conexión para actualizar.")

        try:
            cursor = conexion.cursor()
            
            # 1. Actualizar Persona
            cursor.execute(sql_persona, (
                datos.get("cedula"), datos.get("primer_nombre"), datos.get("primer_apellido"),
                datos.get("telefono"), datos.get("direccion"), datos.get("genero"), 
                datos["persona_id"]
            ))
            
            # 2. Actualizar Personal
            cursor.execute(sql_personal, (
                datos.get("cargo"), datos.get("resolucion"), datos["persona_id"]
            ))
            
            conexion.commit()
            return cursor.rowcount > 0
        except IntegrityError as e:
            raise IntegrityError(f"Error de integridad al actualizar (documento o usuario duplicado). {e}")
        except Error as e:
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
        # Nota: La tabla personal no tiene campo nombre_usuario en el esquema SQLite
        # Esta función necesita ser adaptada según el esquema real
        return None