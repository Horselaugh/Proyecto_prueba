from customtkinter import *
from modulo_Gestion_fami import crear, leer, actualizar, eliminar

def mostrar_resultado(ventana, resultado):
    ventana_resultado = CTkToplevel(ventana)
    ventana_resultado.geometry("800x600")
    ventana_resultado.title("📋 Resultado de la Operación")
    ventana_resultado.configure(fg_color="#2e2e2e")

    texto = CTkTextbox(ventana_resultado, wrap="word", font=("Arial", 12))
    texto.pack(fill="both", expand=True, padx=20, pady=20)
    
    if resultado.get("status") == "success":
        texto.insert("1.0", "✅ Operación exitosa:\n\n")
        if "message" in resultado:
            texto.insert("end", f"📝 {resultado['message']}\n\n")
        if "data" in resultado:
            texto.insert("end", "📊 Datos:\n")
            for row in resultado["data"]:
                texto.insert("end", f"• {str(row)}\n")
    else:
        texto.insert("1.0", "❌ Error:\n\n")
        texto.insert("end", f"⚠️ {resultado.get('error', 'Error desconocido')}")
    
    texto.configure(state="disabled")

def main():
    # Crear ventana principal
    ventana = CTk()
    ventana.geometry("1000x700")
    ventana.title("👨‍👩‍👧‍👦 Gestión de Familiares")
    ventana.configure(fg_color="#2e2e2e")

    # Frame principal
    main_frame = CTkFrame(ventana, fg_color="transparent")
    main_frame.pack(expand=True, fill="both", padx=40, pady=40)

    # Título
    title_label = CTkLabel(
        main_frame, 
        text="👨‍👩‍👧‍👦 GESTIÓN DE FAMILIARES", 
        font=("Arial", 28, "bold"),
        text_color="#3498db"
    )
    title_label.pack(pady=(0, 30))

    # Frame para botones
    buttons_frame = CTkFrame(main_frame, fg_color="transparent")
    buttons_frame.pack(expand=True)

    # Botones de acción con diseño mejorado
    acciones = [
        ("➕ Crear Familiar", "Agregar nuevo familiar al sistema", vista_crear, "#27ae60"),
        ("🔍 Buscar Familiar", "Buscar familiar existente", vista_leer, "#2980b9"),
        ("✏️ Actualizar Familiar", "Modificar datos de familiar", vista_actualizar, "#f39c12"),
        ("🗑️ Eliminar Familiar", "Eliminar familiar del sistema", vista_eliminar, "#e74c3c")
    ]

    for i, (texto, descripcion, comando, color) in enumerate(acciones):
        btn_frame = CTkFrame(buttons_frame, fg_color="transparent")
        btn_frame.pack(pady=15, fill="x", padx=100)
        
        btn = CTkButton(
            btn_frame,
            text=f"{texto}\n{descripcion}",
            command=comando,
            height=70,
            font=("Arial", 16, "bold"),
            fg_color=color,
            hover_color=color,
            text_color="white",
            corner_radius=15
        )
        btn.pack(fill="x")

    # Botón de salir
    exit_frame = CTkFrame(main_frame, fg_color="transparent")
    exit_frame.pack(side="bottom", pady=20)
    
    btn_salir = CTkButton(
        exit_frame,
        text="🚪 Salir",
        command=ventana.destroy,
        height=50,
        font=("Arial", 14),
        fg_color="#7f8c8d",
        hover_color="#95a5a6"
    )
    btn_salir.pack()

    ventana.mainloop()

def vista_crear():
    ventana = CTkToplevel()
    ventana.geometry("900x700")
    ventana.title("➕ Crear Nuevo Familiar")
    ventana.configure(fg_color="#2e2e2e")

    # Frame principal con scroll
    main_frame = CTkScrollableFrame(ventana)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Título
    title_label = CTkLabel(
        main_frame,
        text="➕ CREAR NUEVO FAMILIAR",
        font=("Arial", 24, "bold"),
        text_color="#27ae60"
    )
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))

    # Campos de entrada
    campos = {
        "primer_nombre": CTkEntry(main_frame, placeholder_text="Ej: María", height=40, font=("Arial", 14)),
        "segundo_nombre": CTkEntry(main_frame, placeholder_text="Ej: José", height=40, font=("Arial", 14)),
        "primer_apellido": CTkEntry(main_frame, placeholder_text="Ej: González", height=40, font=("Arial", 14)),
        "segundo_apellido": CTkEntry(main_frame, placeholder_text="Ej: Pérez", height=40, font=("Arial", 14)),
        "direccion": CTkEntry(main_frame, placeholder_text="Ej: Av. Principal #123", height=40, font=("Arial", 14)),
        "telefono": CTkEntry(main_frame, placeholder_text="04141234567 (11 dígitos)", height=40, font=("Arial", 14)),
        "tutor": CTkCheckBox(main_frame, text="👨‍🏫 ¿Es tutor?", font=("Arial", 14))
    }

    labels = [
        ("👤 Primer nombre*:", campos["primer_nombre"]),
        ("👤 Segundo nombre:", campos["segundo_nombre"]),
        ("👤 Primer apellido*:", campos["primer_apellido"]),
        ("👤 Segundo apellido:", campos["segundo_apellido"]),
        ("🏠 Dirección*:", campos["direccion"]),
        ("📞 Teléfono* (11 dígitos):", campos["telefono"]),
        ("", campos["tutor"])
    ]

    for i, (label_text, entry) in enumerate(labels, start=1):
        if label_text:
            CTkLabel(main_frame, text=label_text, font=("Arial", 14)).grid(row=i, column=0, padx=20, pady=15, sticky="e")
        entry.grid(row=i, column=1, padx=20, pady=15, sticky="ew")

    def ejecutar_crear():
        # Validaciones
        if not campos["primer_nombre"].get() or not campos["primer_apellido"].get():
            mostrar_resultado(ventana, {"error": "❌ Primer nombre y primer apellido son obligatorios", "status": "error"})
            return
        
        telefono = campos["telefono"].get()
        if telefono and (len(telefono) != 11 or not telefono.isdigit()):
            mostrar_resultado(ventana, {"error": "❌ El teléfono debe tener exactamente 11 dígitos", "status": "error"})
            return

        resultado = crear(
            primer_nombre=campos["primer_nombre"].get(),
            primer_apellido=campos["primer_apellido"].get(),
            parentesco_id=1,
            direccion=campos["direccion"].get(),
            telefono=telefono,
            segundo_nombre=campos["segundo_nombre"].get() or None,
            segundo_apellido=campos["segundo_apellido"].get() or None,
            tutor=campos["tutor"].get()
        )
        mostrar_resultado(ventana, resultado)

    # Frame para botones
    button_frame = CTkFrame(main_frame, fg_color="transparent")
    button_frame.grid(row=8, column=0, columnspan=2, pady=30)

    btn_crear = CTkButton(
        button_frame,
        text="💾 GUARDAR FAMILIAR",
        command=ejecutar_crear,
        height=50,
        font=("Arial", 16, "bold"),
        fg_color="#27ae60",
        hover_color="#219a52"
    )
    btn_crear.pack(pady=10)

    main_frame.grid_columnconfigure(1, weight=1)

def vista_leer():
    ventana = CTkToplevel()
    ventana.geometry("900x700")
    ventana.title("🔍 Buscar Familiar")
    ventana.configure(fg_color="#2e2e2e")
    ventana.grid_columnconfigure(0, weight=1)

    main_frame = CTkFrame(ventana, fg_color="transparent")
    main_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)
    main_frame.grid_columnconfigure(0, weight=1)

    # Título
    title_label = CTkLabel(
        main_frame,
        text="🔍 BUSCAR FAMILIAR",
        font=("Arial", 24, "bold"),
        text_color="#2980b9"
    )
    title_label.grid(row=0, column=0, pady=(0, 30))

    # Opciones de búsqueda
    CTkLabel(main_frame, text="🔎 Buscar por:", font=("Arial", 16, "bold")).grid(row=1, column=0, sticky="w", pady=10)
    
    opcion_busqueda = StringVar(value="nombre")
    frame_opciones = CTkFrame(main_frame)
    frame_opciones.grid(row=2, column=0, sticky="ew", pady=10)
    
    CTkRadioButton(frame_opciones, text="👤 Nombre y Apellido", variable=opcion_busqueda, value="nombre", font=("Arial", 14)).pack(side="left", padx=20, pady=10)
    CTkRadioButton(frame_opciones, text="🆔 ID del Familiar", variable=opcion_busqueda, value="id", font=("Arial", 14)).pack(side="left", padx=20, pady=10)

    # Frame para campos de búsqueda
    frame_campos = CTkFrame(main_frame)
    frame_campos.grid(row=3, column=0, sticky="nsew", pady=20)
    frame_campos.grid_columnconfigure(1, weight=1)

    current_entries = {}
    
    def mostrar_campos():
        for widget in frame_campos.winfo_children():
            widget.destroy()
        
        if opcion_busqueda.get() == "nombre":
            CTkLabel(frame_campos, text="👤 Primer nombre:", font=("Arial", 14)).grid(row=0, column=0, padx=20, pady=15, sticky="e")
            entry_nombre = CTkEntry(frame_campos, height=40, font=("Arial", 14))
            entry_nombre.grid(row=0, column=1, padx=20, pady=15, sticky="ew")
            
            CTkLabel(frame_campos, text="👤 Primer apellido:", font=("Arial", 14)).grid(row=1, column=0, padx=20, pady=15, sticky="e")
            entry_apellido = CTkEntry(frame_campos, height=40, font=("Arial", 14))
            entry_apellido.grid(row=1, column=1, padx=20, pady=15, sticky="ew")
            
            current_entries["primer_nombre"] = entry_nombre
            current_entries["primer_apellido"] = entry_apellido
        else:
            CTkLabel(frame_campos, text="🆔 ID del Familiar:", font=("Arial", 14)).grid(row=0, column=0, padx=20, pady=15, sticky="e")
            entry_id = CTkEntry(frame_campos, height=40, font=("Arial", 14))
            entry_id.grid(row=0, column=1, padx=20, pady=15, sticky="ew")
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
            id_familiar = current_entries["id"].get() if "id" in current_entries else ""
            if not id_familiar:
                mostrar_resultado(ventana, {"error": "❌ Debe ingresar un ID", "status": "error"})
                return
            resultado = leer(id=id_familiar)
        
        mostrar_resultado(ventana, resultado)

    frame_boton = CTkFrame(main_frame, fg_color="transparent")
    frame_boton.grid(row=4, column=0, sticky="e", pady=20)
    
    btn_leer = CTkButton(
        frame_boton,
        text="🔍 EJECUTAR BÚSQUEDA",
        command=ejecutar_leer,
        height=50,
        font=("Arial", 16, "bold"),
        fg_color="#2980b9",
        hover_color="#2471a3"
    )
    btn_leer.pack()

    ventana.grid_rowconfigure(0, weight=1)

def vista_actualizar():
    ventana = CTkToplevel()
    ventana.geometry("900x800")
    ventana.title("✏️ Actualizar Familiar")
    ventana.configure(fg_color="#2e2e2e")
    
    main_frame = CTkScrollableFrame(ventana)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    main_frame.grid_columnconfigure(1, weight=1)

    # Título
    title_label = CTkLabel(
        main_frame,
        text="✏️ ACTUALIZAR FAMILIAR",
        font=("Arial", 24, "bold"),
        text_color="#f39c12"
    )
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

    # Campo ID obligatorio
    CTkLabel(main_frame, text="🆔 ID del Familiar a actualizar:", font=("Arial", 14, "bold")).grid(row=1, column=0, padx=20, pady=15, sticky="e")
    entry_id = CTkEntry(main_frame, height=40, font=("Arial", 14))
    entry_id.grid(row=1, column=1, padx=20, pady=15, sticky="ew")

    CTkLabel(main_frame, text="📝 Complete solo los campos a actualizar:", font=("Arial", 14)).grid(row=2, column=0, columnspan=2, pady=20)

    # Campos opcionales para actualización
    campos = {
        "primer_nombre": CTkEntry(main_frame, placeholder_text="Nuevo primer nombre", height=40, font=("Arial", 14)),
        "segundo_nombre": CTkEntry(main_frame, placeholder_text="Nuevo segundo nombre", height=40, font=("Arial", 14)),
        "primer_apellido": CTkEntry(main_frame, placeholder_text="Nuevo primer apellido", height=40, font=("Arial", 14)),
        "segundo_apellido": CTkEntry(main_frame, placeholder_text="Nuevo segundo apellido", height=40, font=("Arial", 14)),
        "direccion": CTkEntry(main_frame, placeholder_text="Nueva dirección", height=40, font=("Arial", 14)),
        "telefono": CTkEntry(main_frame, placeholder_text="Nuevo teléfono (11 dígitos)", height=40, font=("Arial", 14)),
        "tutor": CTkCheckBox(main_frame, text="👨‍🏫 ¿Es tutor?", font=("Arial", 14))
    }

    labels = [
        ("👤 Nuevo primer nombre:", campos["primer_nombre"]),
        ("👤 Nuevo segundo nombre:", campos["segundo_nombre"]),
        ("👤 Nuevo primer apellido:", campos["primer_apellido"]),
        ("👤 Nuevo segundo apellido:", campos["segundo_apellido"]),
        ("🏠 Nueva dirección:", campos["direccion"]),
        ("📞 Nuevo teléfono:", campos["telefono"]),
        ("", campos["tutor"])
    ]

    for i, (label_text, entry) in enumerate(labels, start=3):
        if label_text:
            CTkLabel(main_frame, text=label_text, font=("Arial", 14)).grid(row=i, column=0, padx=20, pady=12, sticky="e")
        entry.grid(row=i, column=1, padx=20, pady=12, sticky="ew")

    def ejecutar_actualizar():
        id_familiar = entry_id.get()
        if not id_familiar:
            mostrar_resultado(ventana, {"error": "❌ Debe ingresar un ID", "status": "error"})
            return
        
        # Validar teléfono si se proporciona
        telefono = campos["telefono"].get()
        if telefono and (len(telefono) != 11 or not telefono.isdigit()):
            mostrar_resultado(ventana, {"error": "❌ El teléfono debe tener exactamente 11 dígitos", "status": "error"})
            return
        
        datos_actualizar = {}
        if campos["primer_nombre"].get(): datos_actualizar["primer_nombre"] = campos["primer_nombre"].get()
        if campos["segundo_nombre"].get(): datos_actualizar["segundo_nombre"] = campos["segundo_nombre"].get()
        if campos["primer_apellido"].get(): datos_actualizar["primer_apellido"] = campos["primer_apellido"].get()
        if campos["segundo_apellido"].get(): datos_actualizar["segundo_apellido"] = campos["segundo_apellido"].get()
        if campos["direccion"].get(): datos_actualizar["direccion"] = campos["direccion"].get()
        if telefono: datos_actualizar["telefono"] = telefono
        
        # Para el checkbox, siempre enviar el valor
        datos_actualizar["tutor"] = campos["tutor"].get()
        
        if not datos_actualizar:
            mostrar_resultado(ventana, {"error": "❌ No hay datos para actualizar", "status": "error"})
            return
            
        resultado = actualizar(id_familiar, **datos_actualizar)
        mostrar_resultado(ventana, resultado)

    button_frame = CTkFrame(main_frame, fg_color="transparent")
    button_frame.grid(row=10, column=0, columnspan=2, pady=30)

    btn_actualizar = CTkButton(
        button_frame,
        text="💾 ACTUALIZAR FAMILIAR",
        command=ejecutar_actualizar,
        height=50,
        font=("Arial", 16, "bold"),
        fg_color="#f39c12",
        hover_color="#e67e22"
    )
    btn_actualizar.pack()

def vista_eliminar():
    ventana = CTkToplevel()
    ventana.geometry("600x400")
    ventana.title("🗑️ Eliminar Familiar")
    ventana.configure(fg_color="#2e2e2e")

    main_frame = CTkFrame(ventana, fg_color="transparent")
    main_frame.pack(expand=True, fill="both", padx=40, pady=40)

    # Título
    title_label = CTkLabel(
        main_frame,
        text="🗑️ ELIMINAR FAMILIAR",
        font=("Arial", 24, "bold"),
        text_color="#e74c3c"
    )
    title_label.pack(pady=(0, 30))

    CTkLabel(main_frame, text="🆔 ID del Familiar a eliminar:", font=("Arial", 16)).pack(pady=15)
    entry_id = CTkEntry(main_frame, height=45, font=("Arial", 14))
    entry_id.pack(pady=15, fill="x")

    def ejecutar_eliminar():
        id_familiar = entry_id.get()
        if not id_familiar:
            mostrar_resultado(ventana, {"error": "❌ Debe ingresar un ID", "status": "error"})
            return
        
        confirmacion = CTkToplevel(ventana)
        confirmacion.title("⚠️ Confirmar Eliminación")
        confirmacion.geometry("500x300")
        confirmacion.configure(fg_color="#2e2e2e")
        
        CTkLabel(confirmacion, text=f"¿Eliminar Familiar con ID {id_familiar}?", 
                font=("Arial", 18, "bold")).pack(pady=40)
        
        def confirmar():
            resultado = eliminar(id_familiar)
            mostrar_resultado(ventana, resultado)
            confirmacion.destroy()
        
        frame_botones = CTkFrame(confirmacion, fg_color="transparent")
        frame_botones.pack(pady=30)
        
        CTkButton(frame_botones, text="✅ Sí, eliminar", command=confirmar, 
                 fg_color="#e74c3c", hover_color="#c0392b", height=40,
                 font=("Arial", 14)).pack(side="left", padx=20)
        CTkButton(frame_botones, text="❌ Cancelar", command=confirmacion.destroy,
                 fg_color="#7f8c8d", hover_color="#95a5a6", height=40,
                 font=("Arial", 14)).pack(side="right", padx=20)

    btn_eliminar = CTkButton(
        main_frame,
        text="🗑️ ELIMINAR FAMILIAR",
        command=ejecutar_eliminar,
        height=50,
        font=("Arial", 16, "bold"),
        fg_color="#e74c3c",
        hover_color="#c0392b"
    )
    btn_eliminar.pack(pady=20)

if __name__ == "__main__":
    main()