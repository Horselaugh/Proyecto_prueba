from funcion_base_de_datos import coneccion_db as conec_db, cerrar_coneccion_db as cerrar_db

def crear(nna_id, unidad_id, grado, fecha_matricula=None, activa=True):
    
    # Conexión y operación en BD
    conn = None
    try:
        conn = conec_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO matricula_educativa (nna_id, unidad_id, grado, fecha_matricula, activa) 
            VALUES (?, ?, ?, ?, ?)''',
            (nna_id, unidad_id, grado, fecha_matricula, activa))
        
        conn.commit()
        return {"status": "success", "message": "Matricula creada correctamente"}
    except Exception as e:
        return {"error": str(e), "status": "error"}
    finally:
        if conn:
            cerrar_db(conn)

def leer(nna_id=None, unidad_id=None):
    conn = None
    try:
        conn = conec_db()
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
            return {"error": "No se encontraron registros", "status": "error"}
        return {"data": rows, "status": "success"}
    except Exception as e:
        return {"error": str(e), "status": "error"}
    finally:
        if conn:
            cerrar_db(conn)

def actualizar(nna_id, unidad_id, grado=None, fecha_matricula=None, activa=None):
    updates = {}
    params = []
    
    if grado:
        updates["grado"] = grado
    if fecha_matricula:
        updates["fecha_matricula"] = fecha_matricula
    if activa is not None:
        updates["activa"] = activa
    
    if not updates:
        return {"error": "No hay datos para actualizar", "status": "error"}
    
    set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
    params = list(updates.values())
    params.extend([nna_id, unidad_id])
    
    conn = None
    try:
        conn = conec_db()
        cursor = conn.cursor()
        cursor.execute(f'''
            UPDATE matricula_educativa 
            SET {set_clause} 
            WHERE nna_id = ? AND unidad_id = ?''', params)
        
        conn.commit()
        return {"status": "success", "message": "Matricula actualizada correctamente"}
    except Exception as e:
        return {"error": str(e), "status": "error"}
    finally:
        if conn:
            cerrar_db(conn)

def eliminar(nna_id, unidad_id):
    conn = None
    try:
        conn = conec_db()
        cursor = conn.cursor()
        
        # Verificar existencia
        cursor.execute('SELECT * FROM matricula_educativa WHERE nna_id = ? AND unidad_id = ?', (nna_id, unidad_id))
        if not cursor.fetchone():
            return {"error": "No existe matricula educativa con esos IDs", "status": "error"}
        
        # Eliminar
        cursor.execute('DELETE FROM matricula_educativa WHERE nna_id = ? AND unidad_id = ?', (nna_id, unidad_id))
        conn.commit()
        return {"status": "success", "message": "Matricula educativa eliminada correctamente"}
    except Exception as e:
        return {"error": str(e), "status": "error"}
    finally:
        if conn:
            cerrar_db(conn)