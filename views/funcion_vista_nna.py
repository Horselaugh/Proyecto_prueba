# funcion_vista_nna.py
from customtkinter import *
from modulo_Gestion_NNA import crear, leer, actualizar, eliminar

def mostrar_resultado(ventana, resultado):
    ventana_resultado = CTkToplevel(ventana)
    ventana_resultado.geometry("800x600")
    ventana_resultado.title("📋 Resultado de la Operación")
    ventana_resultado.configure(fg_color="#1e1e1e")
    
    texto = CTkTextbox(ventana_resultado, wrap="word", font=("Arial", 14))
    texto.pack(fill="both", expand=True, padx=20, pady=20)
    
    if resultado.get("status") == "success":
        texto.insert("1.0", "✅ OPERACIÓN EXITOSA\n\n")
        if "message" in resultado:
            texto.insert("end", resultado["message"] + "\n\n")
        if "data" in resultado:
            texto.insert("end", "📊 DATOS ENCONTRADOS:\n")
            texto.insert("end", "="*50 + "\n")
            for row in resultado["data"]:
                texto.insert("end", str(row) + "\n")
    else:
        texto.insert("1.0", "❌ ERROR EN LA OPERACIÓN\n\n")
        texto.insert("end", resultado.get("error", "Error desconocido"))
    
    texto.configure(state="disabled")

def main():
    ventana = CTkToplevel()
    ventana.geometry("1400x900")
    ventana.title("👦 Gestión de NNA (Niños, Niñas y Adolescentes)")
    ventana.configure(fg_color="#1e1e1e")
    
    # Centrar contenido
    frame_principal = CTkFrame(ventana, fg_color="transparent")
    frame_principal.pack(expand=True, fill="both", padx=80, pady=80)
    
    CTkLabel(frame_principal, text="👦 GESTIÓN DE NNA", 
             font=("Arial", 28, "bold")).pack(pady=40)
    
    CTkLabel(frame_principal, text="Niños, Niñas y Adolescentes - Seleccione una operación:", 
             font=("Arial", 18)).pack(pady=30)

    # Frame para botones
    frame_botones = CTkFrame(frame_principal, fg_color="transparent")
    frame_botones.pack(expand=True, pady=40)

    btn_crear = CTkButton(frame_botones, text="➕ CREAR NNA", 
                         command=vista_crear, height=60, width=300,
                         font=("Arial", 18, "bold"), fg_color="#2aa876", hover_color="#228c61")
    btn_crear.pack(pady=20)
    
    btn_leer = CTkButton(frame_botones, text="🔍 BUSCAR NNA", 
                        command=vista_leer, height=60, width=300,
                        font=("Arial", 18, "bold"), fg_color="#3b8ed0", hover_color="#2d70a7")
    btn_leer.pack(pady=20)

    btn_actualizar = CTkButton(frame_botones, text="✏️ ACTUALIZAR NNA", 
                              command=vista_actualizar, height=60, width=300,
                              font=("Arial", 18, "bold"), fg_color="#f0b400", hover_color="#c79500")
    btn_actualizar.pack(pady=20)

    btn_eliminar = CTkButton(frame_botones, text="🗑️ ELIMINAR NNA", 
                            command=vista_eliminar, height=60, width=300,
                            font=("Arial", 18, "bold"), fg_color="#e74c3c", hover_color="#c0392b")
    btn_eliminar.pack(pady=20)

    ventana.mainloop()

def vista_crear():
    ventana = CTkToplevel()
    ventana.geometry("1200x800")
    ventana.title("➕ Crear NNA")
    ventana.configure(fg_color="#1e1e1e")
    ventana.grid_columnconfigure(1, weight=1)

    # Título
    CTkLabel(ventana, text="➕ CREAR NUEVO NNA", 
             font=("Arial", 24, "bold")).grid(row=0, column=0, columnspan=2, pady=30)

    campos = {
        "primer_nombre": CTkEntry(ventana, placeholder_text="👦 Primer nombre", height=45, font=("Arial", 14)),
        "segundo_nombre": CTkEntry(ventana, placeholder_text="👦 Segundo nombre (opcional)", height=45, font=("Arial", 14)),
        "primer_apellido": CTkEntry(ventana, placeholder_text="📝 Primer apellido", height=45, font=("Arial", 14)),
        "segundo_apellido": CTkEntry(ventana, placeholder_text="📝 Segundo apellido (opcional)", height=45, font=("Arial", 14)),
        "fecha_nacimiento": CTkEntry(ventana, placeholder_text="📅 YYYY-MM-DD", height=45, font=("Arial", 14)),
        "genero": CTkOptionMenu(ventana, values=["👦 M", "👧 F"], height=45, font=("Arial", 14)),
        "direccion": CTkEntry(ventana, placeholder_text="🏠 Dirección completa", height=45, font=("Arial", 14)),
        "telefono": CTkEntry(ventana, placeholder_text="📞 11 dígitos", height=45, font=("Arial", 14))
    }

    labels = [
        ("👦 Primer nombre*:", campos["primer_nombre"]),
        ("👦 Segundo nombre:", campos["segundo_nombre"]),
        ("📝 Primer apellido*:", campos["primer_apellido"]),
        ("📝 Segundo apellido:", campos["segundo_apellido"]),
        ("📅 Fecha Nacimiento* (YYYY-MM-DD):", campos["fecha_nacimiento"]),
        ("⚧️ Género*:", campos["genero"]),
        ("🏠 Dirección*:", campos["direccion"]),
        ("📞 Teléfono* (11 dígitos):", campos["telefono"])
    ]

    for i, (label_text, entry) in enumerate(labels, start=1):
        CTkLabel(ventana, text=label_text, font=("Arial", 16)).grid(row=i, column=0, padx=30, pady=15, sticky="e")
        entry.grid(row=i, column=1, padx=30, pady=15, sticky="ew")

    def ejecutar_crear():
        # Validaciones
        if not campos["primer_nombre"].get():
            mostrar_resultado(ventana, {"error": "❌ El primer nombre es obligatorio", "status": "error"})
            return
        if not campos["primer_apellido"].get():
            mostrar_resultado(ventana, {"error": "❌ El primer apellido es obligatorio", "status": "error"})
            return
        if not campos["fecha_nacimiento"].get():
            mostrar_resultado(ventana, {"error": "❌ La fecha de nacimiento es obligatoria", "status": "error"})
            return
        if not campos["direccion"].get():
            mostrar_resultado(ventana, {"error": "❌ La dirección es obligatoria", "status": "error"})
            return
            
        telefono = campos["telefono"].get()
        if not telefono or len(telefono) != 11 or not telefono.isdigit():
            mostrar_resultado(ventana, {"error": "❌ El teléfono debe tener exactamente 11 dígitos", "status": "error"})
            return
            
        # Validar formato de fecha
        fecha = campos["fecha_nacimiento"].get()
        if len(fecha) != 10 or fecha[4] != '-' or fecha[7] != '-':
            mostrar_resultado(ventana, {"error": "❌ Formato de fecha debe ser YYYY-MM-DD", "status": "error"})
            return

        resultado = crear(
            primer_nombre=campos["primer_nombre"].get(),
            primer_apellido=campos["primer_apellido"].get(),
            fecha_nacimiento=campos["fecha_nacimiento"].get(),
            genero=campos["genero"].get().replace("👦 ", "").replace("👧 ", ""),
            direccion=campos["direccion"].get(),
            telefono=telefono,
            segundo_nombre=campos["segundo_nombre"].get() or None,
            segundo_apellido=campos["segundo_apellido"].get() or None
        )
        mostrar_resultado(ventana, resultado)

    btn_crear = CTkButton(ventana, text="🚀 CREAR NNA", command=ejecutar_crear,
                         height=55, font=("Arial", 18, "bold"), fg_color="#2aa876", hover_color="#228c61")
    btn_crear.grid(row=9, column=0, columnspan=2, pady=40)

    ventana.grid_columnconfigure(1, weight=1)

def vista_leer():
    ventana = CTkToplevel()
    ventana.geometry("1200x800")
    ventana.title("🔍 Buscar NNA")
    ventana.configure(fg_color="#1e1e1e")
    ventana.grid_columnconfigure(0, weight=1)

    CTkLabel(ventana, text="🔍 BUSCAR NNA", font=("Arial", 24, "bold")).grid(row=0, column=0, pady=30)
    
    CTkLabel(ventana, text="🔎 Buscar por:", font=("Arial", 18)).grid(row=1, column=0, sticky="w", padx=30, pady=15)
    
    opcion_busqueda = StringVar(value="nombre")
    frame_opciones = CTkFrame(ventana, fg_color="#2e2e2e")
    frame_opciones.grid(row=2, column=0, sticky="ew", padx=30, pady=15)
    
    CTkRadioButton(frame_opciones, text="👤 Nombre y Apellido", variable=opcion_busqueda, value="nombre", font=("Arial", 16)).pack(side="left", padx=25, pady=10)
    CTkRadioButton(frame_opciones, text="🔢 ID", variable=opcion_busqueda, value="id", font=("Arial", 16)).pack(side="left", padx=25, pady=10)

    frame_campos = CTkFrame(ventana, fg_color="#2e2e2e")
    frame_campos.grid(row=3, column=0, sticky="nsew", padx=30, pady=25)
    frame_campos.grid_columnconfigure(1, weight=1)

    current_entries = {}
    
    def mostrar_campos():
        for widget in frame_campos.winfo_children():
            widget.destroy()
        
        if opcion_busqueda.get() == "nombre":
            CTkLabel(frame_campos, text="👦 Primer nombre:", font=("Arial", 16)).grid(row=0, column=0, padx=15, pady=20, sticky="e")
            entry_nombre = CTkEntry(frame_campos, height=45, font=("Arial", 14))
            entry_nombre.grid(row=0, column=1, padx=15, pady=20, sticky="ew")
            
            CTkLabel(frame_campos, text="📝 Primer apellido:", font=("Arial", 16)).grid(row=1, column=0, padx=15, pady=20, sticky="e")
            entry_apellido = CTkEntry(frame_campos, height=45, font=("Arial", 14))
            entry_apellido.grid(row=1, column=1, padx=15, pady=20, sticky="ew")
            
            current_entries["primer_nombre"] = entry_nombre
            current_entries["primer_apellido"] = entry_apellido
        else:
            CTkLabel(frame_campos, text="🔢 ID del NNA:", font=("Arial", 16)).grid(row=0, column=0, padx=15, pady=20, sticky="e")
            entry_id = CTkEntry(frame_campos, height=45, font=("Arial", 14))
            entry_id.grid(row=0, column=1, padx=15, pady=20, sticky="ew")
            current_entries["id"] = entry_id
    
    opcion_busqueda.trace_add("write", lambda *args: mostrar_campos())
    mostrar_campos()

    def ejecutar_leer():
        if opcion_busqueda.get() == "nombre":
            nombre = current_entries["primer_nombre"].get() if "primer_nombre" in current_entries else ""
            apellido = current_entries["primer_apellido"].get() if "primer_apellido" in current_entries else ""
            if not nombre or not apellido:
                mostrar_resultado(ventana, {"error": "❌ Debe ingresar nombre y apellido", "status": "error"})
                return
            resultado = leer(primer_nombre=nombre, primer_apellido=apellido)
        else:
            id_nna = current_entries["id"].get() if "id" in current_entries else ""
            if not id_nna:
                mostrar_resultado(ventana, {"error": "❌ Debe ingresar un ID", "status": "error"})
                return
            resultado = leer(id=id_nna)
        
        mostrar_resultado(ventana, resultado)

    frame_boton = CTkFrame(ventana, fg_color="transparent")
    frame_boton.grid(row=4, column=0, sticky="e", padx=30, pady=25)
    btn_leer = CTkButton(frame_boton, text="🔍 BUSCAR", command=ejecutar_leer,
                        height=55, font=("Arial", 18, "bold"), fg_color="#3b8ed0", hover_color="#2d70a7")
    btn_leer.pack(padx=15, pady=15)

    ventana.grid_rowconfigure(3, weight=1)

def vista_actualizar():
    ventana = CTkToplevel()
    ventana.geometry("1200x800")
    ventana.title("✏️ Actualizar NNA")
    ventana.configure(fg_color="#1e1e1e")
    ventana.grid_columnconfigure(1, weight=1)
    
    main_frame = CTkFrame(ventana, fg_color="#2e2e2e")
    main_frame.grid(row=0, column=0, columnspan=2, padx=30, pady=30, sticky="nsew")
    main_frame.grid_columnconfigure(1, weight=1)

    CTkLabel(main_frame, text="✏️ ACTUALIZAR NNA", font=("Arial", 24, "bold")).grid(row=0, column=0, columnspan=2, pady=25)

    CTkLabel(main_frame, text="🔢 ID del NNA a actualizar:", font=("Arial", 16)).grid(row=1, column=0, padx=15, pady=15, sticky="e")
    entry_id = CTkEntry(main_frame, height=45, font=("Arial", 14))
    entry_id.grid(row=1, column=1, padx=15, pady=15, sticky="ew")

    CTkLabel(main_frame, text="📝 Complete solo los campos a actualizar:", font=("Arial", 16)).grid(row=2, column=0, columnspan=2, pady=20)

    campos = {
        "primer_nombre": CTkEntry(main_frame, placeholder_text="👦 Nuevo primer nombre", height=45, font=("Arial", 14)),
        "segundo_nombre": CTkEntry(main_frame, placeholder_text="👦 Nuevo segundo nombre", height=45, font=("Arial", 14)),
        "primer_apellido": CTkEntry(main_frame, placeholder_text="📝 Nuevo primer apellido", height=45, font=("Arial", 14)),
        "segundo_apellido": CTkEntry(main_frame, placeholder_text="📝 Nuevo segundo apellido", height=45, font=("Arial", 14)),
        "fecha_nacimiento": CTkEntry(main_frame, placeholder_text="📅 YYYY-MM-DD", height=45, font=("Arial", 14)),
        "genero": CTkOptionMenu(main_frame, values=["", "👦 M", "👧 F"], height=45, font=("Arial", 14)),
        "direccion": CTkEntry(main_frame, placeholder_text="🏠 Nueva dirección", height=45, font=("Arial", 14)),
        "telefono": CTkEntry(main_frame, placeholder_text="📞 Nuevo teléfono (11 dígitos)", height=45, font=("Arial", 14))
    }

    labels = [
        ("👦 Nuevo primer nombre:", campos["primer_nombre"]),
        ("👦 Nuevo segundo nombre:", campos["segundo_nombre"]),
        ("📝 Nuevo primer apellido:", campos["primer_apellido"]),
        ("📝 Nuevo segundo apellido:", campos["segundo_apellido"]),
        ("📅 Nueva fecha nacimiento:", campos["fecha_nacimiento"]),
        ("⚧️ Nuevo género:", campos["genero"]),
        ("🏠 Nueva dirección:", campos["direccion"]),
        ("📞 Nuevo teléfono:", campos["telefono"])
    ]

    for i, (label_text, entry) in enumerate(labels, start=3):
        CTkLabel(main_frame, text=label_text, font=("Arial", 16)).grid(row=i, column=0, padx=15, pady=15, sticky="e")
        entry.grid(row=i, column=1, padx=15, pady=15, sticky="ew")

    def ejecutar_actualizar():
        id_nna = entry_id.get()
        if not id_nna:
            mostrar_resultado(ventana, {"error": "❌ Debe ingresar un ID", "status": "error"})
            return
        
        datos_actualizar = {}
        if campos["primer_nombre"].get(): 
            datos_actualizar["primer_nombre"] = campos["primer_nombre"].get()
        if campos["segundo_nombre"].get(): 
            datos_actualizar["segundo_nombre"] = campos["segundo_nombre"].get()
        if campos["primer_apellido"].get(): 
            datos_actualizar["primer_apellido"] = campos["primer_apellido"].get()
        if campos["segundo_apellido"].get(): 
            datos_actualizar["segundo_apellido"] = campos["segundo_apellido"].get()
        if campos["fecha_nacimiento"].get(): 
            fecha = campos["fecha_nacimiento"].get()
            if len(fecha) != 10 or fecha[4] != '-' or fecha[7] != '-':
                mostrar_resultado(ventana, {"error": "❌ Formato de fecha debe ser YYYY-MM-DD", "status": "error"})
                return
            datos_actualizar["fecha_nacimiento"] = fecha
        if campos["genero"].get(): 
            datos_actualizar["genero"] = campos["genero"].get().replace("👦 ", "").replace("👧 ", "")
        if campos["direccion"].get(): 
            datos_actualizar["direccion"] = campos["direccion"].get()
        if campos["telefono"].get(): 
            telefono = campos["telefono"].get()
            if len(telefono) != 11 or not telefono.isdigit():
                mostrar_resultado(ventana, {"error": "❌ El teléfono debe tener exactamente 11 dígitos", "status": "error"})
                return
            datos_actualizar["telefono"] = telefono
        
        if not datos_actualizar:
            mostrar_resultado(ventana, {"error": "❌ No hay datos para actualizar", "status": "error"})
            return
            
        resultado = actualizar(id_nna, **datos_actualizar)
        mostrar_resultado(ventana, resultado)

    button_frame = CTkFrame(ventana, fg_color="transparent")
    button_frame.grid(row=1, column=0, columnspan=2, pady=25)
    btn_actualizar = CTkButton(button_frame, text="✏️ ACTUALIZAR", command=ejecutar_actualizar,
                              height=55, font=("Arial", 18, "bold"), fg_color="#f0b400", hover_color="#c79500")
    btn_actualizar.pack(padx=15, pady=15)

def vista_eliminar():
    ventana = CTkToplevel()
    ventana.geometry("800x500")
    ventana.title("🗑️ Eliminar NNA")
    ventana.configure(fg_color="#1e1e1e")

    frame_principal = CTkFrame(ventana, fg_color="#2e2e2e")
    frame_principal.pack(expand=True, fill="both", padx=40, pady=40)

    CTkLabel(frame_principal, text="🗑️ ELIMINAR NNA", 
             font=("Arial", 24, "bold")).pack(pady=30)

    CTkLabel(frame_principal, text="🔢 ID del NNA a eliminar:", 
             font=("Arial", 18)).pack(pady=20)
    
    entry_id = CTkEntry(frame_principal, height=50, font=("Arial", 16))
    entry_id.pack(pady=20, padx=50, fill="x")

    def ejecutar_eliminar():
        id_nna = entry_id.get()
        if not id_nna:
            mostrar_resultado(ventana, {"error": "❌ Debe ingresar un ID", "status": "error"})
            return
        
        confirmacion = CTkToplevel(ventana)
        confirmacion.title("⚠️ Confirmar Eliminación")
        confirmacion.geometry("500x300")
        confirmacion.configure(fg_color="#1e1e1e")
        
        CTkLabel(confirmacion, text=f"¿Está seguro de eliminar el NNA con ID {id_nna}?", 
                font=("Arial", 16), wraplength=400).pack(pady=40)
        
        def confirmar():
            resultado = eliminar(id_nna)
            mostrar_resultado(ventana, resultado)
            confirmacion.destroy()
        
        frame_botones = CTkFrame(confirmacion, fg_color="transparent")
        frame_botones.pack(pady=30)
        
        CTkButton(frame_botones, text="✅ Sí, Eliminar", command=confirmar, 
                 fg_color="#e74c3c", hover_color="#c0392b", height=45, font=("Arial", 16)).pack(side="left", padx=20)
        CTkButton(frame_botones, text="❌ Cancelar", command=confirmacion.destroy,
                 height=45, font=("Arial", 16)).pack(side="right", padx=20)

    btn_eliminar = CTkButton(frame_principal, text="🗑️ ELIMINAR NNA", command=ejecutar_eliminar,
                            height=55, font=("Arial", 18, "bold"), fg_color="#e74c3c", hover_color="#c0392b")
    btn_eliminar.pack(pady=30)

if __name__ == "__main__":
    main()