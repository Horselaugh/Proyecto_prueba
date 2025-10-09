from funcion_base_de_datos import coneccion_db as conec_db, cerrar_coneccion_db as cerrar_db

def crear(nombre, apellido, fecha_de_nacimiento, genero, direccion, telefono, estado):
    
    # Validaciones
    if len(fecha_de_nacimiento) != 10:
        return {"error": "Fecha debe tener formato YYYY-MM-DD", "status": "error"}
    
    if genero.upper() not in ['MASCULINO', 'FEMENINO', 'OTRO']:
        return {"error": "Género debe ser Masculino/Femenino/Otro", "status": "error"}
    
    if len(telefono) != 11 or not telefono.isdigit():
        return {"error": "Teléfono debe tener 11 dígitos", "status": "error"}
    
    if estado.upper() not in ['ACTIVO', 'EN RIESGO', 'PROTEGIDO']:
        return {"error": "Estado debe ser Activo/En riesgo/Protegido", "status": "error"}

    # Conexión y operación en BD
    conn = None
    try:
        conn = conec_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO NNA (
                NOMBRE_NNA, APELLIDO_NNA, FECHA_NAC_NNA, 
                GENERO_NNA, DIRECCION_NNA, TELEFONO_NNA, ESTADO_NNA
            ) VALUES (?, ?, ?, ?, ?, ?, ?)''', 
            (nombre, apellido, fecha_de_nacimiento, genero.upper(), 
             direccion, telefono, estado.upper()))
        
        conn.commit()
        return {"status": "success", "message": "NNA creado correctamente", "id": cursor.lastrowid}
    except Exception as e:
        return {"error": str(e), "status": "error"}
    finally:
        if conn:
            cerrar_db(conn)

def leer(id=None, nombre=None, apellido=None):
    conn = None
    try:
        conn = conec_db()
        cursor = conn.cursor()
        
        if id:
            cursor.execute('SELECT * FROM NNA WHERE NNA_ID = ?', (id,))
        elif nombre and apellido:
            cursor.execute('''
                SELECT * FROM NNA 
                WHERE NOMBRE_NNA = ? AND APELLIDO_NNA = ?''', 
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

def actualizar(id, nombre=None, apellido=None, fecha_de_nacimiento=None, 
               genero=None, direccion=None, telefono=None, estado=None):
    # Validaciones
    updates = {}
    params = []
    
    if nombre:
        updates["NOMBRE_NNA"] = nombre
    if apellido:
        updates["APELLIDO_NNA"] = apellido
    if fecha_de_nacimiento:
        if len(fecha_de_nacimiento) != 10:
            return {"error": "Fecha debe tener formato YYYY-MM-DD", "status": "error"}
        updates["FECHA_NAC_NNA"] = fecha_de_nacimiento
    if genero:
        if genero.upper() not in ['MASCULINO', 'FEMENINO', 'OTRO']:
            return {"error": "Género no válido", "status": "error"}
        updates["GENERO_NNA"] = genero.upper()
    if direccion:
        updates["DIRECCION_NNA"] = direccion
    if telefono:
        if len(telefono) != 11 or not telefono.isdigit():
            return {"error": "Teléfono debe tener 11 dígitos", "status": "error"}
        updates["TELEFONO_NNA"] = telefono
    if estado:
        if estado.upper() not in ['ACTIVO', 'EN RIESGO', 'PROTEGIDO']:
            return {"error": "Estado no válido", "status": "error"}
        updates["ESTADO_NNA"] = estado.upper()
    
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
            UPDATE NNA 
            SET {set_clause} 
            WHERE NNA_ID = ?''', params)
        
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
        cursor.execute('SELECT * FROM NNA WHERE NNA_ID = ?', (id,))
        if not cursor.fetchone():
            return {"error": "No existe NNA con ese ID", "status": "error"}
        
        # Eliminar
        cursor.execute('DELETE FROM NNA WHERE NNA_ID = ?', (id,))
        conn.commit()
        return {"status": "success", "message": "NNA eliminado correctamente"}
    except Exception as e:
        return {"error": str(e), "status": "error"}
    finally:
        if conn:
            cerrar_db(conn)