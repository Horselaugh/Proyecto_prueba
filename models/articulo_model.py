import sys
import os
# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlite3
from sqlite3 import Row
from typing import List, Optional
from models.database_connector import Database  # Cambiar a nuestro Database
from db_setup import CreateDatabase

class ArticuloModelo:
    """
    Modelo que maneja la estructura de artículos LOPNNA
    """
    def __init__(self):
        self.db = Database()
        self.db = CreateDatabase()
    
    def insertar_articulo(self, codigo: str, articulo: str, descripcion: str) -> Optional[int]:
        """Inserta un artículo y retorna su ID"""
        query = "INSERT INTO articulos (codigo, articulo, descripcion) VALUES (?, ?, ?)"
        try:
            conexion = self.db.crearConexion()
            if not conexion:
                return None
                
            with conexion:
                cursor = conexion.cursor()
                cursor.execute(query, (codigo, articulo, descripcion))
                return cursor.lastrowid
                
        except sqlite3.IntegrityError as e:
            print(f"Advertencia: Artículo {codigo} ya existe. {str(e)}")
            return None
        except sqlite3.Error as e:
            print(f"Error al insertar artículo {codigo}: {str(e)}")
            return None
        finally:
            if conexion:
                self.db.cerrarConexion(conexion)

    def obtener_todos_los_articulos(self) -> List[Row]:
        """
        Retorna todos los artículos para llenar la lista en la vista
        """
        query = """
            SELECT 
                id,
                codigo,
                articulo,
                descripcion
            FROM articulos
            ORDER BY codigo, articulo
        """
        try:
            conexion = self.db.crearConexion()
            if not conexion:
                return []
                
            conexion.row_factory = sqlite3.Row
            cursor = conexion.cursor()
            cursor.execute(query)
            resultado = cursor.fetchall()
            self.db.cerrarConexion(conexion)
            return resultado
            
        except sqlite3.Error as e:
            print(f"Ha ocurrido un error mientras se trataba de obtener todos los artículos: {str(e)}")
            if conexion:
                self.db.cerrarConexion(conexion)
            return []
    
    def buscar_articulo(self, termino_busqueda: str) -> Optional[Row]:
        """Busca y retorna un Artículo por su descripción o por su código"""
        query = """
            SELECT 
                id,
                codigo,
                articulo,
                descripcion
            FROM articulos
            WHERE descripcion LIKE ? OR codigo LIKE ? OR articulo LIKE ?
            ORDER BY codigo, articulo
            LIMIT 1
        """
        
        termino_like = f"%{termino_busqueda}%" 
        parametros = (termino_like, termino_like, termino_like)
        
        try:
            conexion = self.db.crearConexion()
            if not conexion:
                return None
                
            conexion.row_factory = sqlite3.Row
            cursor = conexion.cursor()
            cursor.execute(query, parametros)
            resultado = cursor.fetchone()
            self.db.cerrarConexion(conexion)
            return resultado
            
        except sqlite3.Error as e:
            print(f"Ha ocurrido un error mientras se trataba de obtener el articulo con el término {termino_busqueda}: {str(e)}")
            if conexion:
                self.db.cerrarConexion(conexion)
            return None
    
    def modificar_articulo(self, articulo_id: int, nuevo_codigo: str, nuevo_articulo: str, nueva_descripcion: str) -> bool:
        """
        Modifica los datos de un artículo por su ID.
        """
        query = """
            UPDATE articulos
            SET 
                codigo = ?,
                articulo = ?,
                descripcion = ?
            WHERE id = ?
        """
        
        try:
            conexion = self.db.crearConexion()
            if not conexion:
                return False
                
            with conexion:
                cursor = conexion.cursor()
                parametros = (nuevo_codigo, nuevo_articulo, nueva_descripcion, articulo_id)
                cursor.execute(query, parametros)
                return cursor.rowcount > 0
                
        except sqlite3.IntegrityError as e:
            print(f"Error de integridad: El código {nuevo_codigo} ya existe. {str(e)}")
            return False
        except sqlite3.Error as e:
            print(f"Ha ocurrido un error mientras se trataba actualizar el artículo ID {articulo_id}: {str(e)}")
            return False
        finally:
            if conexion:
                self.db.cerrarConexion(conexion)

    def eliminar_articulo(self, articulo_id: int) -> bool:
        """
        Elimina un artículo de la base de datos dado su ID.
        """
        query = "DELETE FROM articulos WHERE id = ?"
        
        try:
            conexion = self.db.crearConexion()
            if not conexion:
                return False
                
            with conexion:
                cursor = conexion.cursor()
                cursor.execute(query, (articulo_id,))
                if cursor.rowcount > 0:
                    print(f"Artículo ID {articulo_id} eliminado con éxito.")
                    return True
                else:
                    print(f"Advertencia: No se encontró el artículo ID {articulo_id} para eliminar.")
                    return False
                    
        except sqlite3.Error as e:
            print(f"Error al intentar eliminar el artículo ID {articulo_id}: {str(e)}")
            return False
        finally:
            if conexion:
                self.db.cerrarConexion(conexion)