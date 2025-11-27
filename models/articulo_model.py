# models/articulo_model.py
"""
Módulo del modelo para la gestión de artículos (e.g., LOPNNA) en la base de datos.
"""
import sys
import os
import sqlite3
from sqlite3 import Error
from typing import List, Dict, Optional

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from database_connector import Database
except ImportError:
    # Usar ruta relativa si el intento inicial falla (común en ciertos setups)
    from models.database_connector import Database

class ArticuloModelo:
    """
    Modelo que maneja la estructura de artículos LOPNNA
    """
    def __init__(self):
        self.db = Database()
        # self.db.CreateDatabase() # Comentado para corregir E1101 de Pylint.
    
    def insertar_articulo(self, codigo: str, articulo: str, descripcion: str) -> Optional[int]:
        """Inserta un artículo y retorna su ID"""
        query = "INSERT INTO articulos (codigo, articulo, descripcion) VALUES (?, ?, ?)"
        conexion = None
        try:
            conexion = self.db.crearConexion()
            if not conexion:
                return None
                
            cursor = conexion.cursor()
            cursor.execute(query, (codigo, articulo, descripcion))
            conexion.commit()
            return cursor.lastrowid
        # Se manejan IntegrityError (duplicado) y Error general de SQLite
        except sqlite3.IntegrityError as e:
            print(f"Advertencia: Artículo {codigo} ya existe. {str(e)}")
            return None
        except Error as e:
            print(f"Error al insertar artículo {codigo}: {str(e)}")
            return None
        finally:
            if conexion:
                self.db.cerrarConexion(conexion)

    def obtener_todos_los_articulos(self) -> List[Dict]:
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
        conexion = None
        try:
            conexion = self.db.crearConexion()
            if not conexion:
                return []
                
            conexion.row_factory = sqlite3.Row
            cursor = conexion.cursor()
            cursor.execute(query)
            resultado = cursor.fetchall()
            return [dict(row) for row in resultado]
            
        except Error as e:
            print("Ha ocurrido un error mientras se trataba de obtener todos los "
                  f"artículos: {str(e)}")
            return []
        finally:
            if conexion:
                self.db.cerrarConexion(conexion)
    
    def buscar_articulo(self, termino_busqueda: str) -> Optional[Dict]:
        """Busca y retorna un Artículo por su descripción, código o número de artículo"""
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
        
        conexion = None
        try:
            conexion = self.db.crearConexion()
            if not conexion:
                return None
                
            conexion.row_factory = sqlite3.Row
            cursor = conexion.cursor()
            cursor.execute(query, parametros)
            resultado = cursor.fetchone()
            return dict(resultado) if resultado else None
            
        except Error as e:
            print("Ha ocurrido un error mientras se trataba de obtener el "
                  f"articulo: {str(e)}")
            return None
        finally:
            if conexion:
                self.db.cerrarConexion(conexion)
    
    def modificar_articulo(self, articulo_id: int, nuevo_codigo: str, 
                           nuevo_articulo: str, nueva_descripcion: str) -> bool:
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
        
        conexion = None
        try:
            conexion = self.db.crearConexion()
            if not conexion:
                return False
                
            cursor = conexion.cursor()
            parametros = (nuevo_codigo, nuevo_articulo, nueva_descripcion, articulo_id)
            cursor.execute(query, parametros)
            conexion.commit()
            return cursor.rowcount > 0
                
        except sqlite3.IntegrityError as e:
            print(f"Error de integridad: El código {nuevo_codigo} ya existe. {str(e)}")
            return False
        except Error as e:
            print("Ha ocurrido un error mientras se trataba actualizar el "
                  f"artículo ID {articulo_id}: {str(e)}")
            return False
        finally:
            if conexion:
                self.db.cerrarConexion(conexion)

    def eliminar_articulo(self, articulo_id: int) -> bool:
        """
        Elimina un artículo de la base de datos dado su ID.
        """
        query = "DELETE FROM articulos WHERE id = ?"
        
        conexion = None
        try:
            conexion = self.db.crearConexion()
            if not conexion:
                return False
                
            cursor = conexion.cursor()
            cursor.execute(query, (articulo_id,))
            conexion.commit()
            
            if cursor.rowcount > 0:
                print(f"Artículo ID {articulo_id} eliminado con éxito.")
                return True
                
            print(f"Advertencia: No se encontró el artículo ID {articulo_id} para eliminar.")
            return False
                    
        except Error as e:
            print("Error al intentar eliminar el "
                  f"artículo ID {articulo_id}: {str(e)}")
            return False
        finally:
            if conexion:
                self.db.cerrarConexion(conexion)