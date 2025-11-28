# File: seguimiento_expedientes_models.py
import os
import sys
from datetime import datetime, date
from typing import List, Optional, Dict
import sqlite3 # Reemplazo de psycopg2

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from database_connector import Database
except ImportError:
    from models.database_connector import Database

class SeguimientoModel:
    
    def __init__(self):
        # Inicializa la instancia del Singleton de Database
        self.db_connector = Database() 

    def _get_conn(self):
        """Obtiene una conexión a la base de datos SQLite."""
        # Se asegura que la conexión se obtenga a través del Singleton
        return self.db_connector.crearConexion()

    def listar_expedientes(self) -> List[Dict]:
        """
        Obtiene la lista de todos los expedientes disponibles (ID, título, estado).
        """
        # La query asume que la tabla 'expediente' tiene 'id' y 'nna_id' y se usa 'expediente' (singular)
        query = "SELECT id, 'EXPEDIENTE_TITULO_' || nna_id AS titulo, 'ACTIVO' AS estado FROM expediente ORDER BY id ASC;"
        conn = self._get_conn()
        
        if conn is None:
            return []
            
        cur = None
        try:
            # Configurar el cursor para retornar resultados como diccionario (Row object)
            conn.row_factory = sqlite3.Row
            
            cur = conn.cursor()
            cur.execute(query)
            
            # Convertir sqlite3.Row a dict
            rows = [dict(r) for r in cur.fetchall()]
            return rows
        
        except sqlite3.Error as e:
            print(f"AVISO: Error al listar expedientes: {e}. Retornando lista vacía.")
            return []
        
        finally:
            # Asegurar que el cursor se cierre
            if cur:
                cur.close()
            # La conexión no se cierra aquí, ya que la gestiona el Singleton de Database
            
    def registrar_seguimiento(self, expediente_id: int, comentario: str, fecha: Optional[str] = None) -> Dict:
        """Registra un nuevo seguimiento y devuelve un dict con el status."""
        if fecha and fecha.strip():
            try:
                fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
            except Exception as e:
                return {"status": "error", "message": "Formato de fecha inválido. Use YYYY-MM-DD."}
        else:
            fecha_obj = date.today()

        insert_sql = "INSERT INTO seguimiento (expediente_id, fecha, comentario) VALUES (?, ?, ?);"
        conn = self._get_conn()
        
        if conn is None:
             return {"status": "error", "message": "No se pudo establecer conexión con la base de datos."}
             
        cur = None
        try:
            cur = conn.cursor()
            cur.execute(insert_sql, (expediente_id, fecha_obj.strftime("%Y-%m-%d"), comentario))
            
            # Es necesario hacer commit explícito para persistir los cambios en SQLite
            conn.commit()
            new_id = cur.lastrowid # Obtener el ID del último insert
            return {"status": "success", "id": new_id}
            
        except sqlite3.Error as e:
            # Realizar rollback en caso de error de inserción
            conn.rollback()
            return {"status": "error", "message": f"Error al insertar seguimiento: {str(e)}"}
            
        finally:
            if cur:
                cur.close()


    def obtener_seguimientos(self, expediente_id: Optional[int] = None, desde: Optional[str] = None, hasta: Optional[str] = None) -> List[Dict]:
        query = "SELECT id, expediente_id, strftime('%Y-%m-%d', fecha) AS fecha, comentario, creado_en FROM seguimiento WHERE 1=1"
        params = []
        if expediente_id is not None:
            query += " AND expediente_id = ?"
            params.append(expediente_id)
        if desde:
            try:
                datetime.strptime(desde, "%Y-%m-%d")
            except Exception:
                raise ValueError("Parámetro 'desde' con formato inválido. Use YYYY-MM-DD.")
            query += " AND fecha >= ?"
            params.append(desde)
        if hasta:
            try:
                datetime.strptime(hasta, "%Y-%m-%d")
            except Exception:
                raise ValueError("Parámetro 'hasta' con formato inválido. Use YYYY-MM-DD.")
            query += " AND fecha <= ?"
            params.append(hasta)
            
        query += " ORDER BY fecha DESC, creado_en DESC" 
        
        conn = self._get_conn()
        if conn is None:
            return []
            
        cur = None
        try:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(query, tuple(params))
            rows = [dict(r) for r in cur.fetchall()]
            return rows
            
        except sqlite3.Error as e:
            print(f"Error al obtener seguimientos: {e}")
            return []
            
        finally:
            if cur:
                cur.close()


    def obtener_historial_por_expediente(self, expediente_id: int) -> List[Dict]:
        return self.obtener_seguimientos(expediente_id=expediente_id)