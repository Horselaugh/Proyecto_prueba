# base_de_datos/PersonalDAOImpl.py

from base_de_datos.conexion_database import Database
from sqlite3 import Error, IntegrityError
from typing import List, Dict, Optional

# NOTA: Se asume que existe la interfaz PersonalDAO en la carpeta 'dao'
# y la clase Entidad Personal en la carpeta 'models'.

# --- Estructura Simulada (Para Contexto, estas irían en otras carpetas) ---
class PersonalDAO: 
    """Interfaz (Contrato) que define las operaciones del DAO."""
    def agregar_personal(self, datos: dict) -> int: raise NotImplementedError
    def obtener_por_id(self, persona_id: int) -> Optional[dict]: raise NotImplementedError
    def listar_todo(self) -> List[dict]: raise NotImplementedError
    def actualizar_personal(self, datos: dict) -> bool: raise NotImplementedError
    def eliminar_personal(self, persona_id: int) -> bool: raise NotImplementedError
    def obtener_por_usuario(self, nombre_usuario: str) -> Optional[dict]: raise NotImplementedError
# -------------------------------------------------------------------------


class PersonalDAOImpl(PersonalDAO):
    """
    Implementación concreta de las operaciones CRUD para la entidad Personal.
    Depende de la clase Database para la conexión (DIP).
    """
    
    def __init__(self, db_manager: Database):
        self._db_manager = db_manager

    # --------------------------------
    # C R E A T E (Crear)
    # --------------------------------
    def agregar_personal(self, datos: dict) -> int:
        """Inserta un nuevo registro en Persona y Personal dentro de una transacción."""
        
        # 1. Insertar en la tabla persona
        sql_persona = """
        INSERT INTO persona (documento_identidad, primer_nombre, segundo_nombre, 
                             primer_apellido, segundo_apellido, telefono, direccion, genero, activo) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, TRUE)
        """
        # 2. Insertar en la tabla personal
        sql_personal = """
        INSERT INTO personal (persona_id, cargo, resolucion, activo, nombre_usuario, password) 
        VALUES (?, ?, ?, TRUE, ?, ?) 
        """
        
        conexion = self._db_manager.obtener_conexion()
        if conexion is None:
            raise Error("No se pudo establecer conexión con la base de datos.")

        try:
            # Usamos 'with conexion' para manejar la transacción automáticamente (commit/rollback)
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
            # Errores de duplicidad (cédula, teléfono, nombre_usuario)
            raise IntegrityError(f"Error de integridad. El registro ya existe. {e}")
        except Error as e:
            # Otros errores de BD
            raise Error(f"Error de BD al registrar personal: {e}")

    # --------------------------------
    # R E A D (Leer/Consultar)
    # --------------------------------
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
        conexion = self._db_manager.obtener_conexion()
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
        conexion = self._db_manager.obtener_conexion()
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

    # --------------------------------
    # U P D A T E (Actualizar)
    # --------------------------------
    def actualizar_personal(self, datos: dict) -> bool:
        """Actualiza los datos del Personal en ambas tablas."""
        
        # El ID es obligatorio
        if 'persona_id' not in datos:
            return False
            
        # Actualización de Persona
        sql_persona = """
        UPDATE persona SET 
            documento_identidad = ?, primer_nombre = ?, primer_apellido = ?, 
            telefono = ?, direccion = ?, genero = ?
        WHERE id = ?;
        """
        # Actualización de Personal
        sql_personal = """
        UPDATE personal SET 
            cargo = ?, resolucion = ?, nombre_usuario = ?, password = ?
        WHERE persona_id = ?;
        """
        
        conexion = self._db_manager.obtener_conexion()
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
                
                return cursor.rowcount > 0 # Retorna True si se afectó al menos una fila
        except IntegrityError as e:
            raise IntegrityError(f"Error de integridad al actualizar (documento o usuario duplicado). {e}")
        except Error as e:
            raise Error(f"Error de BD al actualizar personal: {e}")

    # --------------------------------
    # D E L E T E (Borrar Lógico)
    # --------------------------------
    def eliminar_personal(self, persona_id: int) -> bool:
        """Realiza un borrado lógico estableciendo el campo 'activo' a FALSE en la tabla persona."""
        
        sql = "UPDATE persona SET activo = FALSE WHERE id = ?;"
        
        conexion = self._db_manager.obtener_conexion()
        if conexion is None:
            raise Error("No se pudo establecer conexión para la eliminación.")

        try:
            with conexion:
                cursor = conexion.cursor()
                cursor.execute(sql, (persona_id,))
                return cursor.rowcount > 0
        except Error as e:
            raise Error(f"Error de BD al eliminar personal: {e}")

    # --------------------------------
    # OPERACIÓN ADICIONAL
    # --------------------------------
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
        conexion = self._db_manager.obtener_conexion()
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