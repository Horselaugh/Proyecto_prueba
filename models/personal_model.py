from sqlite3 import Error, IntegrityError
from typing import List, Dict, Optional

# models/personal_model.py
import sys
import os
# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlite3 import Error, IntegrityError
from typing import List, Dict, Optional

# Ahora importa el módulo database_connector
from database_connector import Database
from db_setup import CreateDatabase

class PersonalModel:
    """Modelo para gestionar las operaciones de Personal en la base de datos"""

    def __init__(self):
        self.db = Database()
        self.db = CreateDatabase()
        
    def _mapear_personal(self, fila: tuple) -> dict:
        """Función interna para mapear una fila de la BD a un diccionario."""
        if not fila:
            return None
        return {
            "persona_id": fila[0],
            "documento_identidad": fila[1],
            "primer_nombre": fila[2],
            "primer_apellido": fila[3],
            "telefono": fila[4],
            "nombre_usuario": fila[5],
            "cargo": fila[6],
            "resolucion": fila[7],
            "activo": bool(fila[8])
        }

    def agregar_personal(self, datos: dict) -> int:
        """Inserta un nuevo registro en Persona y Personal dentro de una transacción."""
        
        sql_persona = """
        INSERT INTO persona (documento_identidad, primer_nombre, segundo_nombre, 
                             primer_apellido, segundo_apellido, telefono, direccion, genero, activo) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, TRUE)
        """
        
        sql_personal = """
        INSERT INTO personal (persona_id, cargo, resolucion, activo, nombre_usuario, password) 
        VALUES (?, ?, ?, TRUE, ?, ?) 
        """
        
        conexion = self.db.crearConexion()
        if conexion is None:
            raise Error("No se pudo establecer conexión con la base de datos.")

        try:
            with conexion:
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
                    datos.get("resolucion"), 
                    datos["nombre_usuario"], 
                    datos["password"]
                ))
                
                return persona_id

        except IntegrityError as e:
            raise IntegrityError(f"Error de integridad. El registro ya existe. {e}")
        except Error as e:
            raise Error(f"Error de BD al registrar personal: {e}")

    def obtener_por_id(self, persona_id: int) -> Optional[dict]:
        """Busca un registro de Personal por su ID."""
        sql = """
        SELECT 
            p.id, p.documento_identidad, p.primer_nombre, p.primer_apellido, 
            p.telefono, pe.nombre_usuario, pe.cargo, pe.resolucion, p.activo
        FROM persona p
        INNER JOIN personal pe ON p.id = pe.persona_id
        WHERE p.id = ?;
        """
        conexion = self.db.crearConexion()
        if conexion is None:
            return None

        try:
            with conexion:
                cursor = conexion.cursor()
                cursor.execute(sql, (persona_id,))
                fila = cursor.fetchone()
                return self._mapear_personal(fila)
        except Error as e:
            raise Error(f"Error al obtener personal por ID: {e}")

    def listar_todo(self) -> List[dict]:
        """Lista todos los registros de Personal activos."""
        sql = """
        SELECT 
            p.id, p.documento_identidad, p.primer_nombre, p.primer_apellido, 
            p.telefono, pe.nombre_usuario, pe.cargo, pe.resolucion, p.activo
        FROM persona p
        INNER JOIN personal pe ON p.id = pe.persona_id
        WHERE p.activo = TRUE;
        """
        conexion = self.db.crearConexion()
        if conexion is None:
            return []

        try:
            with conexion:
                cursor = conexion.cursor()
                cursor.execute(sql)
                filas = cursor.fetchall()
                return [self._mapear_personal(fila) for fila in filas]
        except Error as e:
            raise Error(f"Error al listar personal: {e}")

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
            cargo = ?, resolucion = ?, nombre_usuario = ?, password = ?
        WHERE persona_id = ?;
        """
        
        conexion = self.db.crearConexion()
        if conexion is None:
            raise Error("No se pudo establecer conexión para actualizar.")

        try:
            with conexion:
                cursor = conexion.cursor()
                
                # 1. Actualizar Persona
                cursor.execute(sql_persona, (
                    datos.get("cedula"), datos.get("primer_nombre"), datos.get("primer_apellido"),
                    datos.get("telefono"), datos.get("direccion"), datos.get("genero"), 
                    datos["persona_id"]
                ))
                
                # 2. Actualizar Personal
                cursor.execute(sql_personal, (
                    datos.get("cargo"), datos.get("resolucion"), datos.get("nombre_usuario"), 
                    datos.get("password"), datos["persona_id"]
                ))
                
                return cursor.rowcount > 0
        except IntegrityError as e:
            raise IntegrityError(f"Error de integridad al actualizar (documento o usuario duplicado). {e}")
        except Error as e:
            raise Error(f"Error de BD al actualizar personal: {e}")

    def eliminar_personal(self, persona_id: int) -> bool:
        """Realiza un borrado lógico estableciendo el campo 'activo' a FALSE en la tabla persona."""
        
        sql = "UPDATE persona SET activo = FALSE WHERE id = ?;"
        
        conexion = self.db.crearConexion()
        if conexion is None:
            raise Error("No se pudo establecer conexión para la eliminación.")

        try:
            with conexion:
                cursor = conexion.cursor()
                cursor.execute(sql, (persona_id,))
                return cursor.rowcount > 0
        except Error as e:
            raise Error(f"Error de BD al eliminar personal: {e}")

    def obtener_por_usuario(self, nombre_usuario: str) -> Optional[dict]:
        """Busca un registro de Personal por el nombre de usuario (útil para login)."""
        sql = """
        SELECT 
            p.id, p.documento_identidad, p.primer_nombre, p.primer_apellido, 
            p.telefono, pe.nombre_usuario, pe.cargo, pe.resolucion, p.activo
        FROM persona p
        INNER JOIN personal pe ON p.id = pe.persona_id
        WHERE pe.nombre_usuario = ?;
        """
        conexion = self.db.crearConexion()
        if conexion is None:
            return None

        try:
            with conexion:
                cursor = conexion.cursor()
                cursor.execute(sql, (nombre_usuario,))
                fila = cursor.fetchone()
                return self._mapear_personal(fila)
        except Error as e:
            raise Error(f"Error al obtener personal por nombre de usuario: {e}")