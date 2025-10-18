# matricula_model.py
import sys
import os
from datetime import datetime

# Agregar el directorio actual al path para importar database_connector
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from database_connector import Database

class MatriculaModel:
    def __init__(self):
        self.db = Database()
    
    def _validar_grado(self, grado):
        """Valida que el grado sea válido"""
        # Puedes ajustar esta validación según los grados que manejes
        grados_validos = ['1ro', '2do', '3ro', '4to', '5to', '6to', '1ro Sec', '2do Sec', '3ro Sec', '4to Sec', '5to Sec']
        return grado in grados_validos
    
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
            cursor.execute('SELECT id FROM matricula_educativa WHERE id = ?', (unidad_id,))
            if not cursor.fetchone():
                return False
            
            return True
        except Exception:
            return False
        finally:
            if conn:
                self.db.cerrarConexion()
    
    def crear_matricula(self, nna_id, unidad_id, grado, fecha_matricula=None, activa=True):
        """
        Crea una nueva matrícula educativa en la base de datos
        """
        # Validaciones
        if not nna_id or not unidad_id or not grado:
            return {"error": "NNA ID, Unidad ID y Grado son obligatorios", "status": "error"}
        
        if not self._validar_grado(grado):
            return {"error": "Grado no válido", "status": "error"}
        
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
                (nna_id, unidad_id, grado, fecha_matricula, activa))
            
            conn.commit()
            return {
                "status": "success", 
                "message": "Matrícula creada correctamente",
                "nna_id": nna_id,
                "unidad_id": unidad_id
            }
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e), "status": "error"}
        finally:
            if conn:
                self.db.cerrarConexion()
    
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
                    SELECT me.*, ue.nombre as unidad_nombre, ue.tipo as unidad_tipo
                    FROM matricula_educativa me
                    JOIN unidad_educativa ue ON me.unidad_id = ue.id
                    WHERE me.nna_id = ?''', (nna_id,))
            elif unidad_id:
                cursor.execute('''
                    SELECT me.*, p.primer_nombre, p.primer_apellido, p.documento_identidad
                    FROM matricula_educativa me
                    JOIN persona p ON me.nna_id = p.id
                    WHERE me.unidad_id = ?''', (unidad_id,))
            else:
                return {"error": "Se necesita nna_id y/o unidad_id", "status": "error"}
            
            rows = cursor.fetchall()
            if not rows:
                return {"error": "No se encontraron registros", "status": "error"}
            return {"data": rows, "status": "success"}
        except Exception as e:
            return {"error": str(e), "status": "error"}
        finally:
            if conn:
                self.db.cerrarConexion()
    
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
            updates["activa"] = activa
        
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
            return {"status": "success", "message": "Matrícula actualizada correctamente"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e), "status": "error"}
        finally:
            if conn:
                self.db.cerrarConexion()
    
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
            return {"status": "success", "message": "Matrícula educativa eliminada correctamente"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e), "status": "error"}
        finally:
            if conn:
                self.db.cerrarConexion()
    
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
            return {"data": rows, "status": "success"}
        except Exception as e:
            return {"error": str(e), "status": "error"}
        finally:
            if conn:
                self.db.cerrarConexion()
    
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