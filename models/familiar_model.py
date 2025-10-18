# familiar_model.py
import sys
import os

# Agregar el directorio actual al path para importar database_connector
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from database_connector import Database
from db_setup import CreateDatabase

class FamiliarModel:
    def __init__(self):
        self.db = Database()
        self.db = CreateDatabase()
    
    def _validar_telefono(self, telefono):
        """Valida que el teléfono tenga 11 dígitos"""
        return telefono and len(telefono) == 11 and telefono.isdigit()
    
    def _validar_campos_obligatorios(self, primer_nombre, primer_apellido, parentesco_id):
        """Valida los campos obligatorios"""
        return primer_nombre and primer_apellido and parentesco_id
    
    def crear_familiar(self, primer_nombre, primer_apellido, parentesco_id, direccion, telefono, 
                      segundo_nombre=None, segundo_apellido=None, tutor=False):
        """
        Crea un nuevo familiar en la base de datos
        """
        # Validaciones
        if not self._validar_campos_obligatorios(primer_nombre, primer_apellido, parentesco_id):
            return {"error": "Nombre, apellido y parentesco son obligatorios", "status": "error"}
        
        if not self._validar_telefono(telefono):
            return {"error": "Teléfono debe tener 11 dígitos", "status": "error"}
        
        # Conexión y operación en BD
        conn = None
        try:
            conn = self.db.crearConexion()
            if not conn:
                return {"error": "No se pudo conectar a la base de datos", "status": "error"}
            
            cursor = conn.cursor()
            
            # Primero insertar en persona
            cursor.execute('''
                INSERT INTO persona (
                    documento_identidad, primer_nombre, segundo_nombre, 
                    primer_apellido, segundo_apellido, genero, direccion, telefono
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (None, primer_nombre, segundo_nombre, primer_apellido, 
                 segundo_apellido, 'F', direccion, telefono)
            )
            persona_id = cursor.lastrowid
            
            # Luego insertar en familiar
            cursor.execute('''
                INSERT INTO familiar (persona_id, tutor) 
                VALUES (?, ?)
                ''',
                (persona_id, tutor)
            )
            
            conn.commit()
            return {
                "status": "success", 
                "message": "Familiar creado correctamente", 
                "id": persona_id
            }
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e), "status": "error"}
        finally:
            if conn:
                self.db.cerrarConexion()
    
    def buscar_familiar(self, id=None, primer_nombre=None, primer_apellido=None):
        """
        Busca un familiar por ID o por nombre y apellido
        """
        conn = None
        try:
            conn = self.db.crearConexion()
            if not conn:
                return {"error": "No se pudo conectar a la base de datos", "status": "error"}
            
            cursor = conn.cursor()
            
            if id:
                cursor.execute('''
                    SELECT p.*, f.tutor 
                    FROM persona p 
                    JOIN familiar f ON p.id = f.persona_id 
                    WHERE p.id = ?''', (id,))
            elif primer_nombre and primer_apellido:
                cursor.execute('''
                    SELECT p.*, f.tutor 
                    FROM persona p 
                    JOIN familiar f ON p.id = f.persona_id 
                    WHERE p.primer_nombre = ? AND p.primer_apellido = ?''', 
                    (primer_nombre, primer_apellido))
            else:
                return {"error": "Se necesita ID o nombre y apellido", "status": "error"}
                
            rows = cursor.fetchall()
            if not rows:
                return {"error": "No se encontraron registros", "status": "error"}
            return {"data": rows, "status": "success"}
        except Exception as e:
            return {"error": str(e), "status": "error"}
        finally:
            if conn:
                self.db.cerrarConexion()
    
    def actualizar_familiar(self, id, primer_nombre=None, segundo_nombre=None, primer_apellido=None, 
                           segundo_apellido=None, direccion=None, telefono=None, tutor=None):
        """
        Actualiza los datos de un familiar
        """
        updates = {}
        params = []
        
        # Preparar campos para actualizar
        if primer_nombre:
            updates["primer_nombre"] = primer_nombre
        if segundo_nombre is not None:
            updates["segundo_nombre"] = segundo_nombre
        if primer_apellido:
            updates["primer_apellido"] = primer_apellido
        if segundo_apellido is not None:
            updates["segundo_apellido"] = segundo_apellido
        if direccion:
            updates["direccion"] = direccion
        if telefono:
            if not self._validar_telefono(telefono):
                return {"error": "Teléfono debe tener 11 dígitos", "status": "error"}
            updates["telefono"] = telefono
        
        # Validar que hay datos para actualizar
        if not updates and tutor is None:
            return {"error": "No hay datos para actualizar", "status": "error"}
        
        conn = None
        try:
            conn = self.db.crearConexion()
            if not conn:
                return {"error": "No se pudo conectar a la base de datos", "status": "error"}
            
            cursor = conn.cursor()
            
            # Actualizar persona
            if updates:
                set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
                params = list(updates.values())
                params.append(id)
                cursor.execute(f'UPDATE persona SET {set_clause} WHERE id = ?', params)
            
            # Actualizar familiar si se especifica tutor
            if tutor is not None:
                cursor.execute('UPDATE familiar SET tutor = ? WHERE persona_id = ?', (tutor, id))
            
            conn.commit()
            return {"status": "success", "message": "Familiar actualizado correctamente"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e), "status": "error"}
        finally:
            if conn:
                self.db.cerrarConexion()
    
    def eliminar_familiar(self, id):
        """
        Elimina un familiar de la base de datos
        """
        conn = None
        try:
            conn = self.db.crearConexion()
            if not conn:
                return {"error": "No se pudo conectar a la base de datos", "status": "error"}
            
            cursor = conn.cursor()
            
            # Verificar existencia
            cursor.execute('SELECT * FROM familiar WHERE persona_id = ?', (id,))
            if not cursor.fetchone():
                return {"error": "No existe familiar con ese ID", "status": "error"}
            
            # Eliminar (se eliminará en cascada de la tabla persona)
            cursor.execute('DELETE FROM persona WHERE id = ?', (id,))
            conn.commit()
            return {"status": "success", "message": "Familiar eliminado correctamente"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e), "status": "error"}
        finally:
            if conn:
                self.db.cerrarConexion()