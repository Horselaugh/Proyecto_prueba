from funcion_base_de_datos_fami import coneccion_db as conec_db, cerrar_coneccion_db as cerrar_db

def crear(nombre_familiar, apellido_familiar, relacion_familiar_NNA, direccion_familiar, telefono_familiar):
    # Validaciones
    if not nombre_familiar or not apellido_familiar or not relacion_familiar_NNA:
        return {"error": "Nombre, apellido y relación son obligatorios", "status": "error"}
    if len(telefono_familiar) != 11 or not telefono_familiar.isdigit():
        return {"error": "Teléfono debe tener 11 dígitos", "status": "error"}
    if not relacion_familiar_NNA or len(relacion_familiar_NNA) < 2:
        return {"error": "La relación debe tener al menos 2 caracteres", "status": "error"}
    # Validar caracteres no permitidos
    if any(c in nombre_familiar for c in "'\"\\"):
       return {"error": "Nombre contiene caracteres no permitidos", "status": "error"}
    
    # Conexión y operación en BD
    conn = None
    try:
        conn = conec_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO FAMILIAR(
                NOMBRE_FAMILIAR, 
                APELLIDO_FAMILIAR, 
                RELACION_CON_NNA, 
                DIRECCION_FAMILIAR,
                TELEFONO_FAMILIAR) 
            VALUES (?, ?, ?, ?, ?)''',
            (nombre_familiar, apellido_familiar, relacion_familiar_NNA, direccion_familiar, telefono_familiar))
        
        conn.commit()
        return {"status": "success", "message": "Familiar creado correctamente", "id": cursor.lastrowid}
    except Exception as e:
        return {"error": str(e), "status": "error"}
    finally:
        if conn:
            cerrar_db(conn)

def leer (id=None, nombre=None, apellido=None):
    conn = None
    try:
        conn = conec_db()
        cursor = conn.cursor()
        
        if id:
            cursor.execute('SELECT * FROM FAMILIAR WHERE FAMILIAR_ID = ?', (id,))
        elif nombre and apellido:
            cursor.execute('''
                SELECT * FROM FAMILIAR 
                WHERE NOMBRE_FAMILIAR = ? AND APELLIDO_FAMILIAR = ?''', 
                (nombre, apellido))
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

def actualizar(id, nombre=None, apellido=None, relacion=None, direccion=None, telefono=None):
    # Validaciones
    updates = {}
    params = []
    
    if nombre:
        updates["NOMBRE_FAMILIAR"] = nombre
    if apellido:
        updates["APELLIDO_FAMILIAR"] = apellido
    if direccion:
        updates["DIRECCION_FAMILIAR"] = direccion
    if telefono:
        if len(telefono) != 11 or not telefono.isdigit():
            return {"error": "Teléfono debe tener 11 dígitos", "status": "error"}
        updates["TELEFONO_FAMILIAR"] = telefono
    if relacion:
        updates["RELACION_CON_NNA"] = relacion
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
            UPDATE FAMILIAR 
            SET {set_clause} 
            WHERE FAMILIAR_ID = ?''', params)
        
        conn.commit()
        return {"status": "success", "message": "FAMILIAR actualizado correctamente"}
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
        cursor.execute('SELECT * FROM FAMILIAR WHERE FAMILIAR_ID = ?', (id,))
        if not cursor.fetchone():
            return {"error": "No existe FAMILIAR con ese ID", "status": "error"}
        
        # Eliminar
        cursor.execute('DELETE FROM FAMILIAR WHERE FAMILIAR_ID = ?', (id,))
        conn.commit()
        return {"status": "success", "message": "FAMILIAR eliminado correctamente"}
    except Exception as e:
        return {"error": str(e), "status": "error"}
    finally:
        if conn:
            cerrar_db(conn)