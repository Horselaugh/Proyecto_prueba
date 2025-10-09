from funcion_base_de_datos_UE import coneccion_db as conec_db, cerrar_coneccion_db as cerrar_db

def crear(nombre, nombre_director, tipo, telefono, direccion):
    
    # Validaciones
    if len(telefono) != 11 or not telefono.isdigit():
        return {"error": "Teléfono debe tener 11 dígitos", "status": "error"}
    

    # Conexión y operación en BD
    conn = None
    try:
        conn = conec_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO UNIDAD_EDUCATIVA (NOMBRE_UE, NOMBRE_DIRECTOR_UE, TIPO_UE, TELEFONO_UE, DIRECCION_UE) VALUES (?, ?, ?, ?, ?, ?, ?)''',
            
            (nombre, nombre_director, tipo, telefono, direccion))
        
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
        #BUSCAR POR ID-----------------
        if id:
            cursor.execute('SELECT * FROM UNIDAD_EDUCATIVA WHERE ID_UNIDAD_EDUCATIVA = ?', (id,))
        #BUSCAR POR NOMBRE Y TIPO-----------------
        elif nombre and tipo:
            cursor.execute('''
                SELECT * FROM UNIDAD_EDUCATIVA
                WHERE NOMBRE_UE = ? AND TIPO_UE = ?''', 
                (nombre, tipo))
        else:
            return {"error": "Se necesita ID o nombre y tipo", "status": "error"}
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

def actualizar(id, nombre=None, nombre_director=None, tipo=None, telefono=None, direccion=None):
    # Validaciones
    updates = {}
    params = []
    
    if nombre:
        updates["NOMBRE_UE"] = nombre
    if nombre_director:
        updates["NOMBRE_DIRECTOR_UE"] = nombre_director
    if tipo:
        updates["TIPO_UE"] = tipo
    if telefono:
        if len(telefono) != 11 or not telefono.isdigit():
            return {"error": "Teléfono debe tener 11 dígitos", "status": "error"}
        updates["TELEFONO_UE"] = telefono
    if direccion:
        updates["DIRECCION_UE"] = direccion  
    
    if not updates:
        return {"error": "No hay datos para actualizar", "status": "error"}
    
    # Construir consulta dinámica
    set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
    params = list(updates.values())
    params.append(id)
    
    conn = None
    try:
        conn = conec_db()
        cursor = conn.cursor()
        cursor.execute(f'''
            UPDATE UNIDAD_EDUCATIVA 
            SET {set_clause} 
            WHERE ID_UNIDAD_EDUCATIVA = ?''', params)
        
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
        cursor.execute('SELECT * FROM UNIDAD_EDUCATIVA WHERE ID_UNIDAD_EDUCATIVA = ?', (id,))
        if not cursor.fetchone():
            return {"error": "No existe unidad educativa con ese ID", "status": "error"}
        
        # Eliminar
        cursor.execute('DELETE FROM UNIDAD_EDUCATIVA WHERE ID_UNIDAD_EDUCATIVA = ?', (id,))
        conn.commit()
        return {"status": "success", "message": "Unidad educativa eliminada correctamente"}
    except Exception as e:
        return {"error": str(e), "status": "error"}
    finally:
        if conn:
            cerrar_db(conn)