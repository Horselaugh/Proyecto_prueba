from funcion_base_de_datos import coneccion_db as conec_db, cerrar_coneccion_db as cerrar_db

def crear(primer_nombre, primer_apellido, fecha_nacimiento, genero, direccion, telefono, segundo_nombre=None, segundo_apellido=None):
    
    # Validaciones
    if len(fecha_nacimiento) != 10:
        return {"error": "Fecha debe tener formato YYYY-MM-DD", "status": "error"}
    
    if genero.upper() not in ['M', 'F']:
        return {"error": "Género debe ser M o F", "status": "error"}
    
    if len(telefono) != 11 or not telefono.isdigit():
        return {"error": "Teléfono debe tener 11 dígitos", "status": "error"}

    # Conexión y operación en BD
    conn = None
    try:
        conn = conec_db()
        cursor = conn.cursor()
        
        # Primero insertar en persona
        cursor.execute('''
            INSERT INTO persona.nna (
                documento_identidad, primer_nombre, segundo_nombre, 
                primer_apellido, segundo_apellido, genero, direccion, telefono
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
            (None, primer_nombre, segundo_nombre, primer_apellido, 
             segundo_apellido, genero.upper(), direccion, telefono))
        
        persona_id = cursor.lastrowid
        
        # Luego insertar en nna
        cursor.execute('''
            INSERT INTO nna (persona_id, fecha_nacimiento) 
            VALUES (?, ?)''', 
            (persona_id, fecha_nacimiento))
        
        conn.commit()
        return {"status": "success", "message": "NNA creado correctamente", "id": persona_id}
    except Exception as e:
        return {"error": str(e), "status": "error"}
    finally:
        if conn:
            cerrar_db(conn)

def leer(id=None, primer_nombre=None, primer_apellido=None):
    conn = None
    try:
        conn = conec_db()
        cursor = conn.cursor()
        
        if id:
            cursor.execute('''
                SELECT p.*, n.fecha_nacimiento 
                FROM persona p 
                JOIN nna n ON p.id = n.persona_id 
                WHERE p.id = ?''', (id,))
        elif primer_nombre and primer_apellido:
            cursor.execute('''
                SELECT p.*, n.fecha_nacimiento 
                FROM persona p 
                JOIN nna n ON p.id = n.persona_id 
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
            cerrar_db(conn)

def actualizar(id, primer_nombre=None, segundo_nombre=None, primer_apellido=None, 
               segundo_apellido=None, fecha_nacimiento=None, genero=None, direccion=None, telefono=None):
    updates = {}
    params = []
    
    if primer_nombre:
        updates["primer_nombre"] = primer_nombre
    if segundo_nombre is not None:
        updates["segundo_nombre"] = segundo_nombre
    if primer_apellido:
        updates["primer_apellido"] = primer_apellido
    if segundo_apellido is not None:
        updates["segundo_apellido"] = segundo_apellido
    if genero:
        if genero.upper() not in ['M', 'F']:
            return {"error": "Género no válido", "status": "error"}
        updates["genero"] = genero.upper()
    if direccion:
        updates["direccion"] = direccion
    if telefono:
        if len(telefono) != 11 or not telefono.isdigit():
            return {"error": "Teléfono debe tener 11 dígitos", "status": "error"}
        updates["telefono"] = telefono
    
    if not updates and not fecha_nacimiento:
        return {"error": "No hay datos para actualizar", "status": "error"}
    
    conn = None
    try:
        conn = conec_db()
        cursor = conn.cursor()
        
        # Actualizar persona
        if updates:
            set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
            params = list(updates.values())
            params.append(id)
            cursor.execute(f'UPDATE persona SET {set_clause} WHERE id = ?', params)
        
        # Actualizar nna si se especifica fecha_nacimiento
        if fecha_nacimiento:
            if len(fecha_nacimiento) != 10:
                return {"error": "Fecha debe tener formato YYYY-MM-DD", "status": "error"}
            cursor.execute('UPDATE nna SET fecha_nacimiento = ? WHERE persona_id = ?', (fecha_nacimiento, id))
        
        conn.commit()
        return {"status": "success", "message": "NNA actualizado correctamente"}
    except Exception as e:
        return {"error": str(e), "status": "error"}
    finally:
        if conn:
            cerrar_db(conn)

def eliminar(id):
    conn = None
    try:
        conn = conec_db()
        cursor = conn.cursor()
        
        # Verificar existencia
        cursor.execute('SELECT * FROM nna WHERE persona_id = ?', (id,))
        if not cursor.fetchone():
            return {"error": "No existe NNA con ese ID", "status": "error"}
        
        # Eliminar (se eliminará en cascada de la tabla persona)
        cursor.execute('DELETE FROM persona WHERE id = ?', (id,))
        conn.commit()
        return {"status": "success", "message": "NNA eliminado correctamente"}
    except Exception as e:
        return {"error": str(e), "status": "error"}
    finally:
        if conn:
            cerrar_db(conn)