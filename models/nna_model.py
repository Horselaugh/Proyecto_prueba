# models/nna_model.py
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

class NNAModel:
    """Modelo para gestionar las operaciones de NNA (Niños, Niñas y Adolescentes) en la base de datos"""

    def __init__(self):
        self.db = Database()

    def _mapear_nna(self, fila: dict) -> dict:
        """Función interna para mapear una fila de la BD a un diccionario."""
        if not fila:
            return None
        return {
            "persona_id": fila["id"],
            "documento_identidad": fila["documento_identidad"],
            "primer_nombre": fila["primer_nombre"],
            "segundo_nombre": fila["segundo_nombre"],
            "primer_apellido": fila["primer_apellido"],
            "segundo_apellido": fila["segundo_apellido"],
            "genero": fila["genero"],
            "direccion": fila["direccion"],
            "telefono": fila["telefono"],
            "fecha_nacimiento": fila["fecha_nacimiento"],
            "activo": bool(fila["activo"]) if "activo" in fila else True
        }

    def crear_nna(self, datos: dict) -> dict:
        """Crea un nuevo registro de NNA en la base de datos"""
        
        # Validaciones
        if len(datos["fecha_nacimiento"]) != 10:
            return {"error": "Fecha debe tener formato YYYY-MM-DD", "status": "error"}
        
        if datos["genero"].upper() not in ['M', 'F']:
            return {"error": "Género debe ser M o F", "status": "error"}
        
        if len(datos["telefono"]) != 11 or not datos["telefono"].isdigit():
            return {"error": "Teléfono debe tener 11 dígitos", "status": "error"}

        sql_persona = """
        INSERT INTO persona (
            documento_identidad, primer_nombre, segundo_nombre, 
            primer_apellido, segundo_apellido, genero, direccion, telefono, activo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, TRUE)
        """
        
        sql_nna = """
        INSERT INTO nna (persona_id, fecha_nacimiento) 
        VALUES (?, ?)
        """
        
        conexion = self.db.crearConexion()
        if conexion is None:
            return {"error": "No se pudo establecer conexión con la base de datos", "status": "error"}

        try:
            cursor = conexion.cursor()
            
            # Insertar en persona
            cursor.execute(sql_persona, (
                datos.get("documento_identidad"),
                datos["primer_nombre"],
                datos.get("segundo_nombre"),
                datos["primer_apellido"],
                datos.get("segundo_apellido"),
                datos["genero"].upper(),
                datos["direccion"],
                datos["telefono"]
            ))
            persona_id = cursor.lastrowid
            
            # Insertar en nna
            cursor.execute(sql_nna, (persona_id, datos["fecha_nacimiento"]))
            
            conexion.commit()
            return {
                "status": "success", 
                "message": "NNA creado correctamente", 
                "id": persona_id
            }

        except IntegrityError as e:
            return {"error": f"Error de integridad: {str(e)}", "status": "error"}
        except Error as e:
            return {"error": f"Error de BD al crear NNA: {str(e)}", "status": "error"}
        finally:
            if conexion:
                self.db.cerrarConexion(conexion)

    def obtener_por_id(self, persona_id: int) -> Optional[dict]:
        """Busca un registro de NNA por su ID"""
        sql = """
        SELECT 
            p.id, p.documento_identidad, p.primer_nombre, p.segundo_nombre,
            p.primer_apellido, p.segundo_apellido, p.genero, p.direccion, 
            p.telefono, n.fecha_nacimiento, p.activo
        FROM persona p
        INNER JOIN nna n ON p.id = n.persona_id
        WHERE p.id = ? AND p.activo = TRUE;
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
            print(f"Error al obtener NNA por ID: {e}")
            return None
        finally:
            if conexion:
                self.db.cerrarConexion(conexion)

    def obtener_por_nombre(self, primer_nombre: str, primer_apellido: str) -> List[dict]:
        """Busca registros de NNA por nombre y apellido"""
        sql = """
        SELECT 
            p.id, p.documento_identidad, p.primer_nombre, p.segundo_nombre,
            p.primer_apellido, p.segundo_apellido, p.genero, p.direccion, 
            p.telefono, n.fecha_nacimiento, p.activo
        FROM persona p
        INNER JOIN nna n ON p.id = n.persona_id
        WHERE p.primer_nombre = ? AND p.primer_apellido = ? AND p.activo = TRUE;
        """
        conexion = self.db.crearConexion()
        if conexion is None:
            return []

        try:
            conexion.row_factory = sqlite3.Row
            cursor = conexion.cursor()
            cursor.execute(sql, (primer_nombre, primer_apellido))
            filas = cursor.fetchall()
            return [dict(fila) for fila in filas]
        except Error as e:
            print(f"Error al obtener NNA por nombre: {e}")
            return []
        finally:
            if conexion:
                self.db.cerrarConexion(conexion)

    def listar_todos(self) -> List[dict]:
        """Lista todos los registros de NNA activos"""
        sql = """
        SELECT 
            p.id, p.documento_identidad, p.primer_nombre, p.segundo_nombre,
            p.primer_apellido, p.segundo_apellido, p.genero, p.direccion, 
            p.telefono, n.fecha_nacimiento, p.activo
        FROM persona p
        INNER JOIN nna n ON p.id = n.persona_id
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
            print(f"Error al listar NNA: {e}")
            return []
        finally:
            if conexion:
                self.db.cerrarConexion(conexion)

    def actualizar_nna(self, persona_id: int, datos: dict) -> dict:
        """Actualiza los datos de un NNA"""
        
        updates_persona = {}
        updates_nna = {}
        
        # Preparar actualizaciones para persona
        campos_persona = [
            "primer_nombre", "segundo_nombre", "primer_apellido", "segundo_apellido",
            "genero", "direccion", "telefono", "documento_identidad"
        ]
        
        for campo in campos_persona:
            if campo in datos and datos[campo] is not None:
                updates_persona[campo] = datos[campo]
        
        # Preparar actualizaciones para nna
        if "fecha_nacimiento" in datos and datos["fecha_nacimiento"] is not None:
            if len(datos["fecha_nacimiento"]) != 10:
                return {"error": "Fecha debe tener formato YYYY-MM-DD", "status": "error"}
            updates_nna["fecha_nacimiento"] = datos["fecha_nacimiento"]
        
        # Validaciones
        if "genero" in updates_persona and updates_persona["genero"].upper() not in ['M', 'F']:
            return {"error": "Género debe ser M o F", "status": "error"}
        
        if "telefono" in updates_persona:
            if len(updates_persona["telefono"]) != 11 or not updates_persona["telefono"].isdigit():
                return {"error": "Teléfono debe tener 11 dígitos", "status": "error"}
        
        if not updates_persona and not updates_nna:
            return {"error": "No hay datos para actualizar", "status": "error"}
        
        conexion = self.db.crearConexion()
        if conexion is None:
            return {"error": "No se pudo establecer conexión para actualizar", "status": "error"}

        try:
            cursor = conexion.cursor()
            
            # Actualizar persona si hay cambios
            if updates_persona:
                set_clause = ", ".join([f"{k} = ?" for k in updates_persona.keys()])
                valores = list(updates_persona.values())
                valores.append(persona_id)
                
                cursor.execute(f"UPDATE persona SET {set_clause} WHERE id = ?", valores)
            
            # Actualizar nna si hay cambios
            if updates_nna:
                cursor.execute(
                    "UPDATE nna SET fecha_nacimiento = ? WHERE persona_id = ?",
                    (updates_nna["fecha_nacimiento"], persona_id)
                )
            
            conexion.commit()
            return {"status": "success", "message": "NNA actualizado correctamente"}
                
        except IntegrityError as e:
            return {"error": f"Error de integridad al actualizar: {str(e)}", "status": "error"}
        except Error as e:
            return {"error": f"Error de BD al actualizar NNA: {str(e)}", "status": "error"}
        finally:
            if conexion:
                self.db.cerrarConexion(conexion)

    def eliminar_nna(self, persona_id: int) -> dict:
        """Realiza un borrado lógico del NNA"""
        
        sql = "UPDATE persona SET activo = FALSE WHERE id = ?;"
        
        conexion = self.db.crearConexion()
        if conexion is None:
            return {"error": "No se pudo establecer conexión para eliminar", "status": "error"}

        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (persona_id,))
            conexion.commit()
            
            if cursor.rowcount > 0:
                return {"status": "success", "message": "NNA eliminado correctamente"}
            else:
                return {"error": "No se encontró el NNA con el ID especificado", "status": "error"}
                    
        except Error as e:
            return {"error": f"Error de BD al eliminar NNA: {str(e)}", "status": "error"}
        finally:
            if conexion:
                self.db.cerrarConexion(conexion)