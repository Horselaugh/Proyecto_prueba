from customtkinter import *
from Modulo_Gestion_fami import crear, leer, actualizar, eliminar

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
    ventana = CTk()
    ventana.geometry("400x300")
    ventana.title("Gestión de FAMILIAR")
    ventana.configure(fg_color="#2e2e2e")

    # Botones de acción
    btn_crear = CTkButton(ventana, text="Crear FAMILIAR", command=vista_crear)
    btn_crear.pack(pady=10)
    
    btn_leer = CTkButton(ventana, text="Leer FAMILIAR", command=vista_leer)
    btn_leer.pack(pady=10)

    btn_actualizar = CTkButton(ventana, text="Actualizar FAMILIAR", command=vista_actualizar)
    btn_actualizar.pack(pady=10)

    btn_eliminar = CTkButton(ventana, text="Eliminar FAMILIAR", command=vista_eliminar)
    btn_eliminar.pack(pady=10)

    ventana.mainloop()

def vista_crear():
    # Crear ventana para crear FAMILIAR
    ventana = CTkToplevel()
    ventana.geometry("600x800")
    ventana.title("Crear FAMILIAR")
    ventana.configure(fg_color="#2e2e2e")

    # Campos de entrada
    campos = {
        "nombre": CTkEntry(ventana),
        "apellido": CTkEntry(ventana),
        "relacion": CTkEntry(ventana),
        "direccion": CTkEntry(ventana),
        "telefono": CTkEntry(ventana)
    }

    # Posicionamiento
    for i, (label_text, entry) in enumerate([
        ("Nombre:", campos["nombre"]),
        ("Apellido:", campos["apellido"]),
        ("Relacion:", campos["relacion"]),
        ("Dirección:", campos["direccion"]),
        ("Teléfono:", campos["telefono"])
    ]):
        
        CTkLabel(ventana, text=label_text).grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")

    def ejecutar_crear():
        resultado = crear(
            campos["nombre"].get(),
            campos["apellido"].get(),
            campos["relacion"].get(),
            campos["direccion"].get(),
            campos["telefono"].get()
        )
        mostrar_resultado(ventana, resultado)

    btn_crear = CTkButton(ventana, text="CREAR REGISTRO", command=ejecutar_crear)
    btn_crear.grid(row=7, column=0, columnspan=2, pady=20)

    ventana.grid_columnconfigure(1, weight=1)

def vista_leer():
    ventana = CTkToplevel()
    ventana.geometry("600x400")
    ventana.title("Leer FAMILIAR")
    ventana.configure(fg_color="#2e2e2e")
    ventana.grid_columnconfigure(0, weight=1)

    # Opciones de búsqueda
    CTkLabel(ventana, text="Buscar por:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    
    opcion_busqueda = StringVar(value="nombre")
    frame_opciones = CTkFrame(ventana)
    frame_opciones.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
    
    CTkRadioButton(frame_opciones, text="Nombre y Apellido", variable=opcion_busqueda, value="nombre").pack(side="left", padx=10)
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
        
        if opcion_busqueda.get() == "nombre":
            # Campos para nombre y apellido
            CTkLabel(frame_campos, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
            entry_nombre = CTkEntry(frame_campos)
            entry_nombre.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            
            CTkLabel(frame_campos, text="Apellido:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
            entry_apellido = CTkEntry(frame_campos)
            entry_apellido.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
            
            current_entries["nombre"] = entry_nombre
            current_entries["apellido"] = entry_apellido
        else:
            # Campo para ID
            CTkLabel(frame_campos, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
            entry_id = CTkEntry(frame_campos)
            entry_id.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            
            current_entries["id"] = entry_id
    
    # Configurar el trace
    opcion_busqueda.trace_add("write", lambda *args: mostrar_campos())
    
    # Mostrar campos iniciales
    mostrar_campos()

    def ejecutar_leer():
        if opcion_busqueda.get() == "nombre":
            nombre = current_entries["nombre"].get() if "nombre" in current_entries else ""
            apellido = current_entries["apellido"].get() if "apellido" in current_entries else ""
            if not nombre or not apellido:
                mostrar_resultado(ventana, {"error": "Debe ingresar nombre y apellido", "status": "error"})
                return
            resultado = leer(nombre=nombre, apellido=apellido)
        else:
            id_FAMILIAR = current_entries["id"].get() if "id" in current_entries else ""
            if not id_FAMILIAR:
                mostrar_resultado(ventana, {"error": "Debe ingresar un ID", "status": "error"})
                return
            resultado = leer(id=id_FAMILIAR)
        
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
    ventana.geometry("600x600")
    ventana.title("Actualizar FAMILIAR")
    ventana.configure(fg_color="#2e2e2e")
    
    # Configurar el grid principal
    ventana.grid_columnconfigure(1, weight=1)
    
    # Frame para organizar mejor los elementos
    main_frame = CTkFrame(ventana)
    main_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    main_frame.grid_columnconfigure(1, weight=1)

    # Campo ID obligatorio
    CTkLabel(main_frame, text="ID del FAMILIAR a actualizar:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_id = CTkEntry(main_frame)
    entry_id.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    # Separador
    CTkLabel(main_frame, text="Complete solo los campos a actualizar:").grid(row=1, column=0, columnspan=2, pady=10)

    # Campos opcionales para actualización
    campos = {
        "nombre": CTkEntry(main_frame),
        "apellido": CTkEntry(main_frame),
        "relacion": CTkEntry(main_frame),
        "direccion": CTkEntry(main_frame),
        "telefono": CTkEntry(main_frame)
    }

    # Posicionamiento de los campos
    for i, (label_text, entry) in enumerate([
        ("Nuevo Nombre:", campos["nombre"]),
        ("Nuevo Apellido:", campos["apellido"]),
        ("Nuevo Relacion:", campos["relacion"]),
        ("Nueva Dirección:", campos["direccion"]),
        ("Nuevo Teléfono:", campos["telefono"])
        
    ], start=2):  # Empezar desde la fila 2 para dejar espacio para los elementos anteriores
        CTkLabel(main_frame, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky="e")
        entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")

    # Frame para el botón (para mejor alineación)
    button_frame = CTkFrame(ventana)
    button_frame.grid(row=1, column=0, columnspan=2, pady=10)
    button_frame.grid_columnconfigure(0, weight=1)

    def ejecutar_actualizar():
        id = entry_id.get()
        if not id:
            mostrar_resultado(ventana, {"error": "Debe ingresar un ID", "status": "error"})
            return
        
        # Solo enviar campos que tengan contenido
        datos_actualizar = {}
        if campos["nombre"].get(): datos_actualizar["nombre"] = campos["nombre"].get()
        if campos["apellido"].get(): datos_actualizar["apellido"] = campos["apellido"].get()
        if campos["relacion"].get(): datos_actualizar["relacion"] = campos["relacion"].get()
        if campos["direccion"].get(): datos_actualizar["direccion"] = campos["direccion"].get()
        if campos["telefono"].get(): datos_actualizar["telefono"] = campos["telefono"].get()

        resultado = actualizar(id, **datos_actualizar)
        mostrar_resultado(ventana, resultado)

    btn_actualizar = CTkButton(button_frame, text="ACTUALIZAR", command=ejecutar_actualizar)
    btn_actualizar.grid(row=0, column=0, padx=10, pady=5)

def vista_eliminar():
    # Crear ventana para eliminar FAMILIAR
    ventana = CTkToplevel()
    ventana.geometry("400x200")
    ventana.title("Eliminar FAMILIAR")
    ventana.configure(fg_color="#2e2e2e")

    CTkLabel(ventana, text="ID del FAMILIAR a eliminar:").pack(pady=10)
    entry_id = CTkEntry(ventana)
    entry_id.pack(pady=10)

    def ejecutar_eliminar():
        id_FAMILIAR = entry_id.get()
        if not id_FAMILIAR:
            mostrar_resultado(ventana, {"error": "Debe ingresar un ID", "status": "error"})
            return
        
        # Confirmación
        confirmacion = CTkToplevel(ventana)
        confirmacion.title("Confirmar Eliminación")
        confirmacion.geometry("300x150")
        
        CTkLabel(confirmacion, text=f"¿Eliminar FAMILIAR con ID {id_FAMILIAR}?").pack(pady=20)
        
        def confirmar():
            resultado = eliminar(id_FAMILIAR)
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