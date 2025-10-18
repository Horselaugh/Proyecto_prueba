# models/unidad_educativa_model.py
import sys
import os
import sqlite3

# Agregar el directorio actual al path para importar database_connector
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from database_connector import Database

class UnidadEducativaModel:
    def __init__(self):
        self.db = Database()
    
    def _validar_telefono(self, telefono):
        """Valida que el teléfono tenga 11 dígitos"""
        return telefono and len(telefono) == 11 and telefono.isdigit()
    
    def _validar_tipo(self, tipo):
        """Valida que el tipo sea PUBLICA o PRIVADA"""
        return tipo.upper() in ['PUBLICA', 'PRIVADA']
    
    def _validar_campos_obligatorios(self, nombre, director, tipo, telefono, direccion):
        """Valida los campos obligatorios"""
        return all([nombre, director, tipo, telefono, direccion])
    
    def crear_unidad_educativa(self, nombre, director, tipo, telefono, direccion):
        """
        Crea una nueva unidad educativa en la base de datos
        """
        # Validaciones
        if not self._validar_campos_obligatorios(nombre, director, tipo, telefono, direccion):
            return {"error": "Todos los campos son obligatorios", "status": "error"}
        
        if not self._validar_tipo(tipo):
            return {"error": "Tipo debe ser PUBLICA o PRIVADA", "status": "error"}
        
        if not self._validar_telefono(telefono):
            return {"error": "Teléfono debe tener 11 dígitos", "status": "error"}
        
        # Conexión y operación en BD
        conn = None
        try:
            conn = self.db.crearConexion()
            if not conn:
                return {"error": "No se pudo conectar a la base de datos", "status": "error"}
            
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO unidad_educativa (nombre, director, tipo, telefono, direccion) 
                VALUES (?, ?, ?, ?, ?)''',
                (nombre, director, tipo.upper(), telefono, direccion))
            
            unidad_id = cursor.lastrowid
            conn.commit()
            return {
                "status": "success", 
                "message": "Unidad educativa creada correctamente", 
                "id": unidad_id
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
    
    def buscar_unidad_educativa(self, id=None, nombre=None, tipo=None):
        """
        Busca una unidad educativa por ID, nombre o tipo
        """
        conn = None
        try:
            conn = self.db.crearConexion()
            if not conn:
                return {"error": "No se pudo conectar a la base de datos", "status": "error"}
            
            cursor = conn.cursor()
            
            if id:
                cursor.execute('SELECT * FROM unidad_educativa WHERE id = ?', (id,))
            elif nombre and tipo:
                if not self._validar_tipo(tipo):
                    return {"error": "Tipo debe ser PUBLICA o PRIVADA", "status": "error"}
                cursor.execute('''
                    SELECT * FROM unidad_educativa
                    WHERE nombre = ? AND tipo = ?''', 
                    (nombre, tipo.upper()))
            elif nombre:
                cursor.execute('SELECT * FROM unidad_educativa WHERE nombre = ?', (nombre,))
            else:
                return {"error": "Se necesita ID, nombre o nombre y tipo", "status": "error"}
            
            rows = cursor.fetchall()
            if not rows:
                return {"error": "No se encontraron registros", "status": "error"}
            
            # Convertir a lista de diccionarios
            columns = [description[0] for description in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]
            
            return {"data": result, "status": "success"}
        except Exception as e:
            return {"error": str(e), "status": "error"}
        finally:
            if conn:
                self.db.cerrarConexion(conn)
    
    def actualizar_unidad_educativa(self, id, nombre=None, director=None, tipo=None, telefono=None, direccion=None):
        """
        Actualiza los datos de una unidad educativa
        """
        updates = {}
        params = []
        
        # Preparar campos para actualizar
        if nombre:
            updates["nombre"] = nombre
        if director:
            updates["director"] = director
        if tipo:
            if not self._validar_tipo(tipo):
                return {"error": "Tipo debe ser PUBLICA o PRIVADA", "status": "error"}
            updates["tipo"] = tipo.upper()
        if telefono:
            if not self._validar_telefono(telefono):
                return {"error": "Teléfono debe tener 11 dígitos", "status": "error"}
            updates["telefono"] = telefono
        if direccion:
            updates["direccion"] = direccion
        
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
            params.append(id)
            
            cursor.execute(f'''
                UPDATE unidad_educativa 
                SET {set_clause} 
                WHERE id = ?''', params)
            
            conn.commit()
            
            if cursor.rowcount > 0:
                return {"status": "success", "message": "Unidad educativa actualizada correctamente"}
            else:
                return {"error": "No se encontró la unidad educativa especificada", "status": "error"}
                
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e), "status": "error"}
        finally:
            if conn:
                self.db.cerrarConexion(conn)
    
    def eliminar_unidad_educativa(self, id):
        """
        Elimina una unidad educativa de la base de datos
        """
        conn = None
        try:
            conn = self.db.crearConexion()
            if not conn:
                return {"error": "No se pudo conectar a la base de datos", "status": "error"}
            
            cursor = conn.cursor()
            
            # Verificar existencia
            cursor.execute('SELECT * FROM unidad_educativa WHERE id = ?', (id,))
            if not cursor.fetchone():
                return {"error": "No existe unidad educativa con ese ID", "status": "error"}
            
            # Eliminar
            cursor.execute('DELETE FROM unidad_educativa WHERE id = ?', (id,))
            conn.commit()
            
            if cursor.rowcount > 0:
                return {"status": "success", "message": "Unidad educativa eliminada correctamente"}
            else:
                return {"error": "No se pudo eliminar la unidad educativa", "status": "error"}
                
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e), "status": "error"}
        finally:
            if conn:
                self.db.cerrarConexion(conn)
    
    def listar_todas_unidades_educativas(self):
        """
        Obtiene todas las unidades educativas
        """
        conn = None
        try:
            conn = self.db.crearConexion()
            if not conn:
                return {"error": "No se pudo conectar a la base de datos", "status": "error"}
            
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM unidad_educativa ORDER BY nombre')
            
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