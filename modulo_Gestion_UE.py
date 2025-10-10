from funcion_base_de_datos import coneccion_db as conec_db, cerrar_coneccion_db as cerrar_db

def crear(nombre, director, tipo, telefono, direccion):
    
    # Validaciones
    if len(telefono) != 11 or not telefono.isdigit():
        return {"error": "Teléfono debe tener 11 dígitos", "status": "error"}
    
    if tipo.upper() not in ['PUBLICA', 'PRIVADA']:
        return {"error": "Tipo debe ser PUBLICA o PRIVADA", "status": "error"}

    # Conexión y operación en BD
    conn = None
    try:
        conn = conec_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO unidad_educativa (nombre, director, tipo, telefono, direccion) 
            VALUES (?, ?, ?, ?, ?)''',
            (nombre, director, tipo.upper(), telefono, direccion))
        
        conn.commit()
        return {"status": "success", "message": "UE creado correctamente", "id": cursor.lastrowid}
    except Exception as e:
        return {"error": str(e), "status": "error"}
    finally:
        if conn:
            cerrar_db(conn)

def leer(id=None, nombre=None, tipo=None):
    conn = None
    try:
        conn = conec_db()
        cursor = conn.cursor()
        
        if id:
            cursor.execute('SELECT * FROM unidad_educativa WHERE id = ?', (id,))
        elif nombre and tipo:
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
        return {"data": rows, "status": "success"}
    except Exception as e:
        return {"error": str(e), "status": "error"}
    finally:
        if conn:
            cerrar_db(conn)

def actualizar(id, nombre=None, director=None, tipo=None, telefono=None, direccion=None):
    updates = {}
    params = []
    
    if nombre:
        updates["nombre"] = nombre
    if director:
        updates["director"] = director
    if tipo:
        if tipo.upper() not in ['PUBLICA', 'PRIVADA']:
            return {"error": "Tipo debe ser PUBLICA o PRIVADA", "status": "error"}
        updates["tipo"] = tipo.upper()
    if telefono:
        if len(telefono) != 11 or not telefono.isdigit():
            return {"error": "Teléfono debe tener 11 dígitos", "status": "error"}
        updates["telefono"] = telefono
    if direccion:
        updates["direccion"] = direccion  
    
    if not updates:
        return {"error": "No hay datos para actualizar", "status": "error"}
    
    set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
    params = list(updates.values())
    params.append(id)
    
    conn = None
    try:
        conn = conec_db()
        cursor = conn.cursor()
        cursor.execute(f'''
            UPDATE unidad_educativa 
            SET {set_clause} 
            WHERE id = ?''', params)
        
        conn.commit()
        return {"status": "success", "message": "UE actualizado correctamente"}
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
        cursor.execute('SELECT * FROM unidad_educativa WHERE id = ?', (id,))
        if not cursor.fetchone():
            return {"error": "No existe unidad educativa con ese ID", "status": "error"}
        
        # Eliminar
        cursor.execute('DELETE FROM unidad_educativa WHERE id = ?', (id,))
        conn.commit()
        return {"status": "success", "message": "Unidad educativa eliminada correctamente"}
    except Exception as e:
        return {"error": str(e), "status": "error"}
    finally:
        if conn:
            cerrar_db(conn)