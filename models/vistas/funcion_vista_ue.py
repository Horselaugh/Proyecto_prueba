from customtkinter import *
from Modulo_Gestion_UE import crear, leer, actualizar, eliminar

def mostrar_resultado(ventana, resultado):
    ventana_resultado = CTkToplevel(ventana)
    ventana_resultado.geometry("600x400")
    ventana_resultado.title("Resultado")
    
    texto = CTkTextbox(ventana_resultado, wrap="word")
    texto.pack(fill="both", expand=True, padx=10, pady=10)
    
    if resultado.get("status") == "success":
        texto.insert("1.0", "Operación exitosa:\n\n")
        
        if "message" in resultado:
            texto.insert("end", resultado["message"] + "\n\n")
        
        if "data" in resultado:
            for row in resultado["data"]:
                texto.insert("end", str(row) + "\n")
    else:
        texto.insert("1.0", "Error:\n\n")
        texto.insert("end", resultado.get("error", "Error desconocido"))
    
    texto.configure(state="disabled")

def main():
    # Crear ventana principal
    ventana = CTkToplevel()
    ventana.geometry("400x300")
    ventana.title("Gestión de Unidades Educativas")
    ventana.configure(fg_color="#2e2e2e")

    # Botones de acción
    btn_crear = CTkButton(ventana, text="Crear Unidad Educativa", command=vista_crear)
    btn_crear.pack(pady=10)
    
    btn_leer = CTkButton(ventana, text="Buscar Unidad Educativa", command=vista_leer)
    btn_leer.pack(pady=10)

    btn_actualizar = CTkButton(ventana, text="Actualizar Unidad Educativa", command=vista_actualizar)
    btn_actualizar.pack(pady=10)

    btn_eliminar = CTkButton(ventana, text="Eliminar Unidad Educativa", command=vista_eliminar)
    btn_eliminar.pack(pady=10)

    ventana.mainloop()

def vista_crear():
    # Crear ventana para crear UE
    ventana = CTkToplevel()
    ventana.geometry("600x600")
    ventana.title("Crear Unidad Educativa")
    ventana.configure(fg_color="#2e2e2e")
    
    # Configurar grid
    ventana.grid_columnconfigure(1, weight=1)

    # Campos de entrada para UE
    campos = {
        "nombre": CTkEntry(ventana),
        "nombre_director": CTkEntry(ventana),
        "tipo": CTkOptionMenu(ventana, values=["Pública", "Privada", "Municipal"]),
        "telefono": CTkEntry(ventana, placeholder_text="11 dígitos"),
        "direccion": CTkEntry(ventana)
    }

    # Posicionamiento
    for i, (label_text, entry) in enumerate([
        ("Nombre de la UE:", campos["nombre"]),
        ("Nombre del Director:", campos["nombre_director"]),
        ("Tipo de UE:", campos["tipo"]),
        ("Teléfono (11 dígitos):", campos["telefono"]),
        ("Dirección:", campos["direccion"])
    ]):
        CTkLabel(ventana, text=label_text).grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")

    def ejecutar_crear():
        # Validar teléfono antes de enviar
        telefono = campos["telefono"].get()
        if len(telefono) != 11 or not telefono.isdigit():
            mostrar_resultado(ventana, {"error": "Teléfono debe tener exactamente 11 dígitos", "status": "error"})
            return
            
        resultado = crear(
            campos["nombre"].get(),
            campos["nombre_director"].get(),
            campos["tipo"].get(),
            telefono,
            campos["direccion"].get()
        )
        mostrar_resultado(ventana, resultado)

    btn_crear = CTkButton(ventana, text="CREAR UNIDAD EDUCATIVA", command=ejecutar_crear)
    btn_crear.grid(row=5, column=0, columnspan=2, pady=20)

    ventana.grid_columnconfigure(1, weight=1)

def vista_leer():
    ventana = CTkToplevel()
    ventana.geometry("600x400")
    ventana.title("Buscar Unidad Educativa")
    ventana.configure(fg_color="#2e2e2e")
    ventana.grid_columnconfigure(0, weight=1)

    # Opciones de búsqueda
    CTkLabel(ventana, text="Buscar por:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    
    opcion_busqueda = StringVar(value="nombre_tipo")
    frame_opciones = CTkFrame(ventana)
    frame_opciones.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
    
    CTkRadioButton(frame_opciones, text="Nombre y Tipo", variable=opcion_busqueda, value="nombre_tipo").pack(side="left", padx=10)
    CTkRadioButton(frame_opciones, text="ID", variable=opcion_busqueda, value="id").pack(side="left", padx=10)

    # Frame para campos de búsqueda
    frame_campos = CTkFrame(ventana)
    frame_campos.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
    frame_campos.grid_columnconfigure(1, weight=1)

    # Variables para almacenar las entradas
    current_entries = {}
    
    def mostrar_campos():
        # Limpiar el frame
        for widget in frame_campos.winfo_children():
            widget.destroy()
        
        if opcion_busqueda.get() == "nombre_tipo":
            # Campos para nombre y tipo
            CTkLabel(frame_campos, text="Nombre UE:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
            entry_nombre = CTkEntry(frame_campos)
            entry_nombre.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            
            CTkLabel(frame_campos, text="Tipo UE:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
            entry_tipo = CTkOptionMenu(frame_campos, values=["Pública", "Privada", "Municipal"])
            entry_tipo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
            
            current_entries["nombre"] = entry_nombre
            current_entries["tipo"] = entry_tipo
        else:
            # Campo para ID
            CTkLabel(frame_campos, text="ID UE:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
            entry_id = CTkEntry(frame_campos)
            entry_id.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            
            current_entries["id"] = entry_id
    
    # Configurar el trace
    opcion_busqueda.trace_add("write", lambda *args: mostrar_campos())
    
    # Mostrar campos iniciales
    mostrar_campos()

    def ejecutar_leer():
        if opcion_busqueda.get() == "nombre_tipo":
            nombre = current_entries["nombre"].get() if "nombre" in current_entries else ""
            tipo = current_entries["tipo"].get() if "tipo" in current_entries else ""
            if not nombre or not tipo:
                mostrar_resultado(ventana, {"error": "Debe ingresar nombre y tipo", "status": "error"})
                return
            resultado = leer(nombre=nombre, tipo=tipo)
        else:
            id_ue = current_entries["id"].get() if "id" in current_entries else ""
            if not id_ue:
                mostrar_resultado(ventana, {"error": "Debe ingresar un ID", "status": "error"})
                return
            resultado = leer(id=id_ue)
        
        mostrar_resultado(ventana, resultado)

    # Frame para el botón
    frame_boton = CTkFrame(ventana)
    frame_boton.grid(row=3, column=0, sticky="e", padx=10, pady=10)
    
    btn_leer = CTkButton(frame_boton, text="BUSCAR", command=ejecutar_leer)
    btn_leer.pack(padx=10, pady=5)

    # Configurar el peso de las filas
    ventana.grid_rowconfigure(2, weight=1)

def vista_actualizar():
    ventana = CTkToplevel()
    ventana.geometry("600x500")
    ventana.title("Actualizar Unidad Educativa")
    ventana.configure(fg_color="#2e2e2e")
    
    # Configurar el grid principal
    ventana.grid_columnconfigure(1, weight=1)
    
    # Frame para organizar mejor los elementos
    main_frame = CTkFrame(ventana)
    main_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    main_frame.grid_columnconfigure(1, weight=1)

    # Campo ID obligatorio
    CTkLabel(main_frame, text="ID de la UE a actualizar:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_id = CTkEntry(main_frame)
    entry_id.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    # Separador
    CTkLabel(main_frame, text="Complete solo los campos a actualizar:").grid(row=1, column=0, columnspan=2, pady=10)

    # Campos opcionales para actualización
    campos = {
        "nombre": CTkEntry(main_frame),
        "nombre_director": CTkEntry(main_frame),
        "tipo": CTkOptionMenu(main_frame, values=["", "Pública", "Privada", "Municipal"]),
        "telefono": CTkEntry(main_frame, placeholder_text="11 dígitos"),
        "direccion": CTkEntry(main_frame)
    }

    # Posicionamiento de los campos
    for i, (label_text, entry) in enumerate([
        ("Nuevo Nombre UE:", campos["nombre"]),
        ("Nuevo Nombre Director:", campos["nombre_director"]),
        ("Nuevo Tipo UE:", campos["tipo"]),
        ("Nuevo Teléfono:", campos["telefono"]),
        ("Nueva Dirección:", campos["direccion"])
    ], start=2):
        CTkLabel(main_frame, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky="e")
        entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")

    # Frame para el botón
    button_frame = CTkFrame(ventana)
    button_frame.grid(row=1, column=0, columnspan=2, pady=10)
    button_frame.grid_columnconfigure(0, weight=1)

    def ejecutar_actualizar():
        id_ue = entry_id.get()
        if not id_ue:
            mostrar_resultado(ventana, {"error": "Debe ingresar un ID", "status": "error"})
            return
        
        # Validar teléfono si se proporciona
        telefono = campos["telefono"].get()
        if telefono and (len(telefono) != 11 or not telefono.isdigit()):
            mostrar_resultado(ventana, {"error": "Teléfono debe tener exactamente 11 dígitos", "status": "error"})
            return
        
        # Solo enviar campos que tengan contenido
        datos_actualizar = {}
        if campos["nombre"].get(): datos_actualizar["nombre"] = campos["nombre"].get()
        if campos["nombre_director"].get(): datos_actualizar["nombre_director"] = campos["nombre_director"].get()
        if campos["tipo"].get(): datos_actualizar["tipo"] = campos["tipo"].get()
        if telefono: datos_actualizar["telefono"] = telefono
        if campos["direccion"].get(): datos_actualizar["direccion"] = campos["direccion"].get()
        
        if not datos_actualizar:
            mostrar_resultado(ventana, {"error": "No hay datos para actualizar", "status": "error"})
            return
            
        resultado = actualizar(id_ue, **datos_actualizar)
        mostrar_resultado(ventana, resultado)

    btn_actualizar = CTkButton(button_frame, text="ACTUALIZAR", command=ejecutar_actualizar)
    btn_actualizar.grid(row=0, column=0, padx=10, pady=5)

def vista_eliminar():
    # Crear ventana para eliminar UE
    ventana = CTkToplevel()
    ventana.geometry("400x200")
    ventana.title("Eliminar Unidad Educativa")
    ventana.configure(fg_color="#2e2e2e")

    CTkLabel(ventana, text="ID de la UE a eliminar:").pack(pady=10)
    entry_id = CTkEntry(ventana)
    entry_id.pack(pady=10)

    def ejecutar_eliminar():
        id_ue = entry_id.get()
        if not id_ue:
            mostrar_resultado(ventana, {"error": "Debe ingresar un ID", "status": "error"})
            return
        
        # Confirmación
        confirmacion = CTkToplevel(ventana)
        confirmacion.title("Confirmar Eliminación")
        confirmacion.geometry("300x150")
        
        CTkLabel(confirmacion, text=f"¿Eliminar UE con ID {id_ue}?").pack(pady=20)
        
        def confirmar():
            resultado = eliminar(id_ue)
            mostrar_resultado(ventana, resultado)
            confirmacion.destroy()
        
        frame_botones = CTkFrame(confirmacion)
        frame_botones.pack(pady=10)
        
        CTkButton(frame_botones, text="Sí", command=confirmar).pack(side="left", padx=10)
        CTkButton(frame_botones, text="No", command=confirmacion.destroy).pack(side="right", padx=10)

    btn_eliminar = CTkButton(ventana, text="ELIMINAR", command=ejecutar_eliminar)
    btn_eliminar.pack(pady=10)

if __name__ == "__main__":
    main()