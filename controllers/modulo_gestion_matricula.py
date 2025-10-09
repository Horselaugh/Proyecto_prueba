from funcion_base_de_datos_matricula import coneccion_db as conec_db, cerrar_coneccion_db as cerrar_db

def crear(grado, fecha_matricula, activa):
    
    # Conexión y operación en BD
    conn = None
    try:
        conn = conec_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO MATRICULA_EDUCATIVA (GRADO_MATRICULA, FECHA_MATRICULA, ACTIVA_MATRICULA) VALUES (?, ?, ?, ?, ?, ?, ?)''',
            
            (grado, fecha_matricula, activa))
        
        conn.commit()
        return {"status": "success", "message": "Matricula creada correctamente", "id": cursor.lastrowid}
    except Exception as e:
        return {"error": str(e), "status": "error"}
    finally:
        if conn:
            cerrar_db(conn)

def leer(id=None, grado=None, fecha_matricula=None):
    conn = None
    try:
        conn = conec_db()
        cursor = conn.cursor()
        #BUSCAR POR ID-----------------
        if id:
            cursor.execute('SELECT * FROM MATRICULA_EDUCATIVA WHERE ID_MATRICULA_EDUCATIVA = ?', (id,))
        #BUSCAR POR NOMBRE Y TIPO-----------------
        elif grado and fecha_matricula:
            cursor.execute('''
                SELECT * FROM MATRICULA_EDUCATIVA
                WHERE GRADO_MATRICULA = ? AND FECHA_MATRICULA = ?''', 
                (grado, fecha_matricula))
        else:
            return {"error": "Se necesita ID o grado y fecha", "status": "error"}
        #SI NO SE ENCUENTRAN REGISTROS-----------------
        rows = cursor.fetchall()
        if not rows:
            return {"error": "No se encontraron registros", "status": "error"}
        return {"data": rows, "status": "success"}
    except Exception as e:
        return {"error": str(e), "status": "error"}
    finally:
        if conn:
            cerrar_db(conn)

def actualizar(id=None, grado=None, fecha_matricula=None, activa=None):
    # Validaciones
    updates = {}
    params = []
    
    if grado:
        updates["GRADO_MATRICULA"] = grado
    if fecha_matricula:
        updates["FECHA_MATRICULA"] = fecha_matricula
    if activa:
        updates["ACTIVA_MATRICULA"] = activa
    
    # Construir consulta dinámica
    set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
    params = list(updates.values())
    params.append(id)
    
    conn = None
    try:
        conn = conec_db()
        cursor = conn.cursor()
        cursor.execute(f'''
            UPDATE MATRICULA_EDUCATIVA 
            SET {set_clause} 
            WHERE ID_MATRICULA_EDUCATIVA = ?''', params)
        
        conn.commit()
        return {"status": "success", "message": "Matricula actualizado correctamente"}
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
        cursor.execute('SELECT * FROM MATRICULA_EDUCATIVA WHERE ID_MATRICULA_EDUCATIVA = ?', (id,))
        if not cursor.fetchone():
            return {"error": "No existe matricula educativa con ese ID", "status": "error"}
        
        # Eliminar
        cursor.execute('DELETE FROM MATRICULA_EDUCATIVA WHERE ID_MATRICULA_EDUCATIVA = ?', (id,))
        conn.commit()
        return {"status": "success", "message": "Matricula educativa eliminada correctamente"}
    except Exception as e:
        return {"error": str(e), "status": "error"}
    finally:
        if conn:
            cerrar_db(conn)