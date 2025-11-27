# models/matricula_model.py
import sys
import os
import sqlite3
from datetime import datetime

# Asumiendo que 'database_connector' es accesible o se debe importar
current_dir = os.path.dirname(os.path.abspath(__file__))
# Asumiendo que database_connector.py está en el directorio superior (ej. al nivel de 'models')
sys.path.append(os.path.join(current_dir, '..')) 
try:
    from database_connector import Database
except ImportError:
    # Esto es un placeholder si no existe Database, para que el código compile
    class Database:
        def crearConexion(self): 
             # Simulación de error de conexión si no existe
             print("ADVERTENCIA: No se pudo importar Database. Las operaciones de BD fallarán.")
             return None 
        def cerrarConexion(self, conn): pass


class MatriculaModel:
    def __init__(self):
        self.db = Database()
    
    def _validar_grado(self, grado):
        """Valida que el grado sea válido"""
        grados_validos = ['1ro', '2do', '3ro', '4to', '5to', '6to', '1ro Sec', '2do Sec', '3ro Sec', '4to Sec', '5to Sec']
        return grado in grados_validos

    def obtener_nna(self):
        """
        Obtiene la lista de todos los NNA (Niños, Niñas y Adolescentes).
        """
        conn = None
        try:
            conn = self.db.crearConexion()
            if not conn:
                return []
            
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido 
                FROM persona 
                WHERE tipo_persona = 'NNA' OR rol = 'NNA' 
                ORDER BY primer_apellido
            ''')
            
            rows = cursor.fetchall()
            
            # Formatear el resultado para la vista (id y nombre_completo)
            result = []
            for row in rows:
                id_nna, nombre1, nombre2, apellido1, apellido2 = row
                nombre_completo = f"{nombre1} {nombre2 if nombre2 else ''} {apellido1} {apellido2 if apellido2 else ''}".strip().replace("  ", " ")
                result.append({"id": id_nna, "nombre_completo": nombre_completo})
                
            return result
        except Exception as e:
            print(f"Error al obtener NNA: {str(e)}")
            return []
        finally:
            if conn:
                self.db.cerrarConexion(conn)

    def obtener_unidades_educativas(self):
        """
        Obtiene la lista de todas las unidades educativas.
        """
        conn = None
        try:
            conn = self.db.crearConexion()
            if not conn:
                return []
            
            cursor = conn.cursor()
            cursor.execute('SELECT id, nombre, codigo FROM unidad_educativa ORDER BY nombre')
            
            rows = cursor.fetchall()
            
            # Formatear el resultado (id, nombre, codigo)
            columns = [description[0] for description in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]
                
            return result
        except Exception as e:
            print(f"Error al obtener Unidades Educativas: {str(e)}")
            return []
        finally:
            if conn:
                self.db.cerrarConexion(conn)
    
    def listar_grados(self):
        """
        Retorna la lista de grados escolares válidos.
        """
        return ['1ro', '2do', '3ro', '4to', '5to', '6to', '1ro Sec', '2do Sec', '3ro Sec', '4to Sec', '5to Sec']
    
    def _validar_ids(self, nna_id, unidad_id):
        """Valida que los IDs existan en la base de datos"""
        conn = None
        try:
            conn = self.db.crearConexion()
            if not conn:
                return False
            
            cursor = conn.cursor()
            
            # Verificar que el NNA existe
            cursor.execute('SELECT id FROM persona WHERE id = ?', (nna_id,))
            if not cursor.fetchone():
                return False
            
            # Verificar que la unidad educativa existe
            cursor.execute('SELECT id FROM unidad_educativa WHERE id = ?', (unidad_id,))
            if not cursor.fetchone():
                return False
            
            return True
        except Exception:
            return False
        finally:
            if conn:
                self.db.cerrarConexion(conn)
    
    def crear_matricula(self, nna_id, unidad_id, grado, fecha_matricula=None, activa=True):
        """
        Crea una nueva matrícula educativa en la base de datos
        """
        # Validaciones
        if not nna_id or not unidad_id or not grado:
            return {"error": "NNA ID, Unidad ID y Grado son obligatorios", "status": "error"}
        
        if not self._validar_grado(grado):
            return {"error": "Grado no válido", "status": "error"}
        
        if not self._validar_ids(nna_id, unidad_id):
            return {"error": "NNA ID o Unidad ID no existen", "status": "error"}
        
        # Si no se proporciona fecha, usar la fecha actual
        if not fecha_matricula:
            fecha_matricula = datetime.now().strftime('%Y-%m-%d')
        
        # Conexión y operación en BD
        conn = None
        try:
            conn = self.db.crearConexion()
            if not conn:
                return {"error": "No se pudo conectar a la base de datos", "status": "error"}
            
            cursor = conn.cursor()
            
            # Verificar si ya existe una matrícula activa para este NNA
            cursor.execute('''
                SELECT * FROM matricula_educativa 
                WHERE nna_id = ? AND activa = 1
            ''', (nna_id,))
            
            if cursor.fetchone():
                return {"error": "El NNA ya tiene una matrícula activa", "status": "error"}
            
            # Insertar nueva matrícula
            cursor.execute('''
                INSERT INTO matricula_educativa (nna_id, unidad_id, grado, fecha_matricula, activa) 
                VALUES (?, ?, ?, ?, ?)''',
                (nna_id, unidad_id, grado, fecha_matricula, 1 if activa else 0))
            
            conn.commit()
            return {
                "status": "success", 
                "message": "Matrícula creada correctamente",
                "nna_id": nna_id,
                "unidad_id": unidad_id
            }
        except sqlite3.IntegrityError as e:
            if conn:
                conn.rollback()
            return {"error": f"Error de integridad: {str(e)}", "status": "error"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e), "status": "error"}
        finally:
            if conn:
                self.db.cerrarConexion(conn)
    
    def buscar_matricula(self, nna_id=None, unidad_id=None):
        """
        Busca matrículas por NNA ID, Unidad ID o ambos
        """
        conn = None
        try:
            conn = self.db.crearConexion()
            if not conn:
                return {"error": "No se pudo conectar a la base de datos", "status": "error"}
            
            cursor = conn.cursor()
            
            if nna_id and unidad_id:
                cursor.execute('''
                    SELECT me.*, p.primer_nombre, p.primer_apellido, ue.nombre as unidad_nombre
                    FROM matricula_educativa me
                    JOIN persona p ON me.nna_id = p.id
                    JOIN unidad_educativa ue ON me.unidad_id = ue.id
                    WHERE me.nna_id = ? AND me.unidad_id = ?''', 
                    (nna_id, unidad_id))
            elif nna_id:
                cursor.execute('''
                    SELECT me.*, ue.nombre as unidad_nombre
                    FROM matricula_educativa me
                    JOIN unidad_educativa ue ON me.unidad_id = ue.id
                    WHERE me.nna_id = ?''', (nna_id,))
            elif unidad_id:
                cursor.execute('''
                    SELECT me.*, p.primer_nombre, p.primer_apellido
                    FROM matricula_educativa me
                    JOIN persona p ON me.nna_id = p.id
                    WHERE me.unidad_id = ?''', (unidad_id,))
            else:
                return {"error": "Se necesita nna_id y/o unidad_id", "status": "error"}
            
            rows = cursor.fetchall()
            if not rows:
                return {"data": [], "status": "success", "message": "No se encontraron registros"}
            
            # Convertir a lista de diccionarios
            columns = [description[0] for description in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]
            
            return {"data": result, "status": "success"}
        except Exception as e:
            return {"error": str(e), "status": "error"}
        finally:
            if conn:
                self.db.cerrarConexion(conn)
    
    def actualizar_matricula(self, nna_id, unidad_id, grado=None, fecha_matricula=None, activa=None):
        """
        Actualiza los datos de una matrícula educativa
        """
        updates = {}
        params = []
        
        # Preparar campos para actualizar
        if grado:
            if not self._validar_grado(grado):
                return {"error": "Grado no válido", "status": "error"}
            updates["grado"] = grado
        if fecha_matricula:
            updates["fecha_matricula"] = fecha_matricula
        if activa is not None:
            updates["activa"] = 1 if activa else 0
        
        # Validar que hay datos para actualizar
        if not updates:
            return {"error": "No hay datos para actualizar", "status": "error"}
        
        conn = None
        try:
            conn = self.db.crearConexion()
            if not conn:
                return {"error": "No se pudo conectar a la base de datos", "status": "error"}
            
            cursor = conn.cursor()
            
            set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
            params = list(updates.values())
            params.extend([nna_id, unidad_id])
            
            cursor.execute(f'''
                UPDATE matricula_educativa 
                SET {set_clause} 
                WHERE nna_id = ? AND unidad_id = ?''', params)
            
            conn.commit()
            
            if cursor.rowcount > 0:
                return {"status": "success", "message": "Matrícula actualizada correctamente"}
            else:
                return {"error": "No se encontró la matrícula especificada", "status": "error"}
                
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e), "status": "error"}
        finally:
            if conn:
                self.db.cerrarConexion(conn)
    
    def eliminar_matricula(self, nna_id, unidad_id):
        """
        Elimina una matrícula educativa de la base de datos
        """
        conn = None
        try:
            conn = self.db.crearConexion()
            if not conn:
                return {"error": "No se pudo conectar a la base de datos", "status": "error"}
            
            cursor = conn.cursor()
            
            # Verificar existencia
            cursor.execute('SELECT * FROM matricula_educativa WHERE nna_id = ? AND unidad_id = ?', (nna_id, unidad_id))
            if not cursor.fetchone():
                return {"error": "No existe matrícula educativa con esos IDs", "status": "error"}
            
            # Eliminar
            cursor.execute('DELETE FROM matricula_educativa WHERE nna_id = ? AND unidad_id = ?', (nna_id, unidad_id))
            conn.commit()
            
            if cursor.rowcount > 0:
                return {"status": "success", "message": "Matrícula educativa eliminada correctamente"}
            else:
                return {"error": "No se pudo eliminar la matrícula", "status": "error"}
                
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e), "status": "error"}
        finally:
            if conn:
                self.db.cerrarConexion(conn)
    
    def listar_matriculas_activas(self):
        """
        Obtiene todas las matrículas activas
        """
        conn = None
        try:
            conn = self.db.crearConexion()
            if not conn:
                return {"error": "No se pudo conectar a la base de datos", "status": "error"}
            
            cursor = conn.cursor()
            cursor.execute('''
                SELECT me.*, p.primer_nombre, p.primer_apellido, ue.nombre as unidad_nombre
                FROM matricula_educativa me
                JOIN persona p ON me.nna_id = p.id
                JOIN unidad_educativa ue ON me.unidad_id = ue.id
                WHERE me.activa = 1
                ORDER BY ue.nombre, p.primer_apellido
            ''')
            
            rows = cursor.fetchall()
            
            # Convertir a lista de diccionarios
            columns = [description[0] for description in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]
            
            return {"data": result, "status": "success"}
        except Exception as e:
            return {"error": str(e), "status": "error"}
        finally:
            if conn:
                self.db.cerrarConexion(conn)
    
    def obtener_matricula_por_nna(self, nna_id):
        """
        Obtiene todas las matrículas de un NNA específico
        """
        return self.buscar_matricula(nna_id=nna_id)
    
    def obtener_matriculas_por_unidad(self, unidad_id):
        """
        Obtiene todas las matrículas de una unidad educativa específica
        """
        return self.buscar_matricula(unidad_id=unidad_id)