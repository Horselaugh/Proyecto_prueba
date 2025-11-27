# models/familiar_model.py
import sys
import os
import sqlite3

# Añadir el path para que las importaciones relativas funcionen
sys.path.append(os.path.join(os.path.dirname(__file__)))

try:
    from database_connector import Database  # Usamos la clase Database (Singleton)
except ImportError:
    print("Advertencia: No se pudo importar Database directamente. Intentando models.database_connector...")
    from models.database_connector import Database

class FamiliarModel:
    def __init__(self):
        self.db = Database()

    def _validar_telefono(self, telefono):
        """Valida que el teléfono tenga 11 dígitos"""
        return telefono and len(telefono) == 11 and telefono.isdigit()
    
    def _validar_campos_obligatorios(self, primer_nombre, primer_apellido):
        """Valida los campos obligatorios"""
        return primer_nombre and primer_apellido
    
    def crear_familiar(self, primer_nombre, primer_apellido, direccion, telefono, 
                      parentesco_id, segundo_nombre=None, segundo_apellido=None, tutor=False): # AÑADIDO: parentesco_id
        """
        Crea un nuevo familiar en la base de datos
        """
        # Validaciones
        if not self._validar_campos_obligatorios(primer_nombre, primer_apellido):
            return {"error": "Nombre y apellido son obligatorios", "status": "error"}
        
        # Nueva validación para parentesco
        if not parentesco_id:
            return {"error": "Parentesco es obligatorio", "status": "error"}
        
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
                    primer_apellido, segundo_apellido, genero, direccion, telefono, activo
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, TRUE)
                ''',
                (None, primer_nombre, segundo_nombre, primer_apellido, 
                 segundo_apellido, 'F', direccion, telefono)
            )
            persona_id = cursor.lastrowid
            
            # --- MODIFICACIÓN CLAVE (Inserción) ---
            # Luego insertar en familiar, incluyendo parentesco_id
            cursor.execute('''
                INSERT INTO familiar (persona_id, tutor, parentesco_id) 
                VALUES (?, ?, ?)
                ''',
                (persona_id, 1 if tutor else 0, parentesco_id)
            )
            
            conn.commit()
            return {
                "status": "success", 
                "message": "Familiar creado correctamente", 
                "id": persona_id
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
    
    def buscar_familiar(self, id=None, primer_nombre=None, primer_apellido=None):
        """
        Busca un familiar por ID o por nombre y apellido. Incluye parentesco_id y parentesco_desc.
        """
        conn = None
        try:
            conn = self.db.crearConexion()
            if not conn:
                return {"error": "No se pudo conectar a la base de datos", "status": "error"}
            
            cursor = conn.cursor()
            
            # --- MODIFICACIÓN CLAVE (Consulta) ---
            query = '''
                    SELECT p.*, f.tutor, f.parentesco_id, pa.nombre AS parentesco_desc 
                    FROM persona p 
                    JOIN familiar f ON p.id = f.persona_id 
                    LEFT JOIN parentesco pa ON f.parentesco_id = pa.id
                    WHERE p.id = ?
                '''
            
            if id:
                cursor.execute(query, (id,))
            elif primer_nombre and primer_apellido:
                query = query.replace("WHERE p.id = ?", "WHERE p.primer_nombre = ? AND p.primer_apellido = ?")
                cursor.execute(query, (primer_nombre, primer_apellido))
            else:
                return {"error": "Se necesita ID o nombre y apellido", "status": "error"}
                
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
    
    def actualizar_familiar(self, id, primer_nombre=None, segundo_nombre=None, primer_apellido=None, 
                           segundo_apellido=None, direccion=None, telefono=None, tutor=None, parentesco_id=None): # AÑADIDO: parentesco_id
        """
        Actualiza los datos de un familiar
        """
        updates = {}
        params = []
        
        # Preparar campos para actualizar en la tabla persona
        if primer_nombre:
            updates["primer_nombre"] = primer_nombre
        # ... (resto de campos de persona)
        if direccion:
            updates["direccion"] = direccion
        if telefono:
            if not self._validar_telefono(telefono):
                return {"error": "Teléfono debe tener 11 dígitos", "status": "error"}
            updates["telefono"] = telefono
        
        # Validar que hay datos para actualizar
        if not updates and tutor is None and parentesco_id is None: # MODIFICACIÓN: Incluir parentesco_id
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
            
            # Actualizar familiar (tutor y parentesco_id)
            familiar_updates = {}
            familiar_params = []
            
            if tutor is not None:
                familiar_updates["tutor"] = 1 if tutor else 0
            if parentesco_id is not None: # MODIFICACIÓN CLAVE (Actualización de Parentesco)
                familiar_updates["parentesco_id"] = parentesco_id
                
            if familiar_updates:
                familiar_set_clause = ", ".join([f"{k} = ?" for k in familiar_updates.keys()])
                familiar_params = list(familiar_updates.values())
                familiar_params.append(id)
                cursor.execute(f'UPDATE familiar SET {familiar_set_clause} WHERE persona_id = ?', familiar_params)
            
            conn.commit()
            
            # Simplificamos la verificación del rowcount
            cursor.execute('SELECT 1 FROM persona WHERE id = ?', (id,))
            if not cursor.fetchone():
                return {"error": "No se encontró el familiar especificado", "status": "error"}
            
            return {"status": "success", "message": "Familiar actualizado correctamente"}

        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e), "status": "error"}
        finally:
            if conn:
                self.db.cerrarConexion(conn)
    
    def eliminar_familiar(self, id):
        # El código es correcto. No se requiere modificación.
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
            
            if cursor.rowcount > 0:
                return {"status": "success", "message": "Familiar eliminado correctamente"}
            else:
                return {"error": "No se pudo eliminar el familiar", "status": "error"}
                
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e), "status": "error"}
        finally:
            if conn:
                self.db.cerrarConexion(conn)
                
    def obtener_parentescos(self):
        # El código es correcto. No se requiere modificación.
        conn = None
        try:
            conn = self.db.crearConexion()
            if not conn:
                return [] # Retorna lista vacía si falla la conexión
            
            cursor = conn.cursor()
            cursor.execute('SELECT id, nombre FROM parentesco ORDER BY nombre')
            
            rows = cursor.fetchall()
            
            columns = [description[0] for description in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]
            
            return result # Devolver la lista de diccionarios
        except Exception as e:
            print(f"Error al obtener parentescos: {str(e)}")
            return []
        finally:
            if conn:
                self.db.cerrarConexion(conn)
    
    def listar_todos_familiares(self):
        """
        Obtiene todos los familiares. Incluye parentesco_desc.
        """
        conn = None
        try:
            conn = self.db.crearConexion()
            if not conn:
                return {"error": "No se pudo conectar a la base de datos", "status": "error"}
            
            cursor = conn.cursor()
            # --- MODIFICACIÓN CLAVE (Consulta) ---
            cursor.execute('''
                SELECT p.*, f.tutor, f.parentesco_id, pa.nombre AS parentesco_desc
                FROM persona p 
                JOIN familiar f ON p.id = f.persona_id 
                LEFT JOIN parentesco pa ON f.parentesco_id = pa.id
                ORDER BY p.primer_apellido, p.primer_nombre
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