# funcion_vista_ue.py
from customtkinter import *
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controllers.unidad_educativa_controller import crear, leer, actualizar, eliminar

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
    # Crear ventana principal
    ventana = CTkToplevel()
    ventana.geometry("1400x900")
    ventana.title("🏫 Gestión de Unidades Educativas")
    ventana.configure(fg_color="#1e1e1e")
    
    # Centrar contenido
    frame_principal = CTkFrame(ventana, fg_color="transparent")
    frame_principal.pack(expand=True, fill="both", padx=80, pady=80)
    
    CTkLabel(frame_principal, text="🏫 GESTIÓN DE UNIDADES EDUCATIVAS", 
             font=("Arial", 28, "bold")).pack(pady=40)
    
    CTkLabel(frame_principal, text="Seleccione una operación:", 
             font=("Arial", 18)).pack(pady=30)

    # Frame para botones
    frame_botones = CTkFrame(frame_principal, fg_color="transparent")
    frame_botones.pack(expand=True, pady=40)

    # Botones de acción
    btn_crear = CTkButton(frame_botones, text="➕ CREAR UNIDAD EDUCATIVA", 
                         command=vista_crear, height=60, width=300,
                         font=("Arial", 18, "bold"), fg_color="#2aa876", hover_color="#228c61")
    btn_crear.pack(pady=20)
    
    btn_leer = CTkButton(frame_botones, text="🔍 BUSCAR UNIDAD EDUCATIVA", 
                        command=vista_leer, height=60, width=300,
                        font=("Arial", 18, "bold"), fg_color="#3b8ed0", hover_color="#2d70a7")
    btn_leer.pack(pady=20)

    btn_actualizar = CTkButton(frame_botones, text="✏️ ACTUALIZAR UNIDAD EDUCATIVA", 
                              command=vista_actualizar, height=60, width=300,
                              font=("Arial", 18, "bold"), fg_color="#f0b400", hover_color="#c79500")
    btn_actualizar.pack(pady=20)

    btn_eliminar = CTkButton(frame_botones, text="🗑️ ELIMINAR UNIDAD EDUCATIVA", 
                            command=vista_eliminar, height=60, width=300,
                            font=("Arial", 18, "bold"), fg_color="#e74c3c", hover_color="#c0392b")
    btn_eliminar.pack(pady=20)

    ventana.mainloop()

def vista_crear():
    # Crear ventana para crear UE
    ventana = CTkToplevel()
    ventana.geometry("1200x800")
    ventana.title("➕ Crear Unidad Educativa")
    ventana.configure(fg_color="#1e1e1e")
    
    # Configurar grid
    ventana.grid_columnconfigure(1, weight=1)

    # Título
    CTkLabel(ventana, text="➕ CREAR NUEVA UNIDAD EDUCATIVA", 
             font=("Arial", 24, "bold")).grid(row=0, column=0, columnspan=2, pady=30)

    # Campos de entrada para UE
    campos = {
        "nombre": CTkEntry(ventana, placeholder_text="🏫 Nombre de la unidad educativa", height=45, font=("Arial", 14)),
        "nombre_director": CTkEntry(ventana, placeholder_text="👨‍💼 Nombre del director", height=45, font=("Arial", 14)),
        "tipo": CTkOptionMenu(ventana, values=["🏛️ Pública", "💼 Privada", "🏢 Municipal"], height=45, font=("Arial", 14)),
        "telefono": CTkEntry(ventana, placeholder_text="📞 11 dígitos", height=45, font=("Arial", 14)),
        "direccion": CTkEntry(ventana, placeholder_text="📍 Dirección completa", height=45, font=("Arial", 14))
    }

    # Posicionamiento
    for i, (label_text, entry) in enumerate([
        ("🏫 Nombre de la UE*:", campos["nombre"]),
        ("👨‍💼 Nombre del Director*:", campos["nombre_director"]),
        ("🏛️ Tipo de UE*:", campos["tipo"]),
        ("📞 Teléfono* (11 dígitos):", campos["telefono"]),
        ("📍 Dirección*:", campos["direccion"])
    ], start=1):
        CTkLabel(ventana, text=label_text, font=("Arial", 16)).grid(row=i, column=0, padx=30, pady=15, sticky="e")
        entry.grid(row=i, column=1, padx=30, pady=15, sticky="ew")

    def ejecutar_crear():
        # Validaciones
        if not campos["nombre"].get():
            mostrar_resultado(ventana, {"error": "❌ El nombre de la UE es obligatorio", "status": "error"})
            return
        if not campos["nombre_director"].get():
            mostrar_resultado(ventana, {"error": "❌ El nombre del director es obligatorio", "status": "error"})
            return
        if not campos["direccion"].get():
            mostrar_resultado(ventana, {"error": "❌ La dirección es obligatoria", "status": "error"})
            return
            
        # Validar teléfono antes de enviar
        telefono = campos["telefono"].get()
        if len(telefono) != 11 or not telefono.isdigit():
            mostrar_resultado(ventana, {"error": "❌ El teléfono debe tener exactamente 11 dígitos", "status": "error"})
            return
            
        resultado = crear(
            campos["nombre"].get(),
            campos["nombre_director"].get(),
            campos["tipo"].get().replace("🏛️ ", "").replace("💼 ", "").replace("🏢 ", ""),
            telefono,
            campos["direccion"].get()
        )
        mostrar_resultado(ventana, resultado)

    btn_crear = CTkButton(ventana, text="🚀 CREAR UNIDAD EDUCATIVA", command=ejecutar_crear,
                         height=55, font=("Arial", 18, "bold"), fg_color="#2aa876", hover_color="#228c61")
    btn_crear.grid(row=6, column=0, columnspan=2, pady=40)

    ventana.grid_columnconfigure(1, weight=1)

def vista_leer():
    ventana = CTkToplevel()
    ventana.geometry("1200x800")
    ventana.title("🔍 Buscar Unidad Educativa")
    ventana.configure(fg_color="#1e1e1e")
    ventana.grid_columnconfigure(0, weight=1)

    # Título
    CTkLabel(ventana, text="🔍 BUSCAR UNIDAD EDUCATIVA", font=("Arial", 24, "bold")).grid(row=0, column=0, pady=30)

    # Opciones de búsqueda
    CTkLabel(ventana, text="🔎 Buscar por:", font=("Arial", 18)).grid(row=1, column=0, sticky="w", padx=30, pady=15)
    
    opcion_busqueda = StringVar(value="nombre_tipo")
    frame_opciones = CTkFrame(ventana, fg_color="#2e2e2e")
    frame_opciones.grid(row=2, column=0, sticky="ew", padx=30, pady=15)
    
    CTkRadioButton(frame_opciones, text="🏫 Nombre y Tipo", variable=opcion_busqueda, value="nombre_tipo", font=("Arial", 16)).pack(side="left", padx=25, pady=10)
    CTkRadioButton(frame_opciones, text="🔢 ID", variable=opcion_busqueda, value="id", font=("Arial", 16)).pack(side="left", padx=25, pady=10)

    # Frame para campos de búsqueda
    frame_campos = CTkFrame(ventana, fg_color="#2e2e2e")
    frame_campos.grid(row=3, column=0, sticky="nsew", padx=30, pady=25)
    frame_campos.grid_columnconfigure(1, weight=1)

    # Variables para almacenar las entradas
    current_entries = {}
    
    def mostrar_campos():
        # Limpiar el frame
        for widget in frame_campos.winfo_children():
            widget.destroy()
        
        if opcion_busqueda.get() == "nombre_tipo":
            # Campos para nombre y tipo
            CTkLabel(frame_campos, text="🏫 Nombre UE:", font=("Arial", 16)).grid(row=0, column=0, padx=15, pady=20, sticky="e")
            entry_nombre = CTkEntry(frame_campos, height=45, font=("Arial", 14))
            entry_nombre.grid(row=0, column=1, padx=15, pady=20, sticky="ew")
            
            CTkLabel(frame_campos, text="🏛️ Tipo UE:", font=("Arial", 16)).grid(row=1, column=0, padx=15, pady=20, sticky="e")
            entry_tipo = CTkOptionMenu(frame_campos, values=["🏛️ Pública", "💼 Privada", "🏢 Municipal"], height=45, font=("Arial", 14))
            entry_tipo.grid(row=1, column=1, padx=15, pady=20, sticky="ew")
            
            current_entries["nombre"] = entry_nombre
            current_entries["tipo"] = entry_tipo
        else:
            # Campo para ID
            CTkLabel(frame_campos, text="🔢 ID UE:", font=("Arial", 16)).grid(row=0, column=0, padx=15, pady=20, sticky="e")
            entry_id = CTkEntry(frame_campos, height=45, font=("Arial", 14))
            entry_id.grid(row=0, column=1, padx=15, pady=20, sticky="ew")
            
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
                mostrar_resultado(ventana, {"error": "❌ Debe ingresar nombre y tipo", "status": "error"})
                return
            resultado = leer(nombre=nombre, tipo=tipo.replace("🏛️ ", "").replace("💼 ", "").replace("🏢 ", ""))
        else:
            id_ue = current_entries["id"].get() if "id" in current_entries else ""
            if not id_ue:
                mostrar_resultado(ventana, {"error": "❌ Debe ingresar un ID", "status": "error"})
                return
            resultado = leer(id=id_ue)
        
        mostrar_resultado(ventana, resultado)

    # Frame para el botón
    frame_boton = CTkFrame(ventana, fg_color="transparent")
    frame_boton.grid(row=4, column=0, sticky="e", padx=30, pady=25)
    
    btn_leer = CTkButton(frame_boton, text="🔍 BUSCAR", command=ejecutar_leer,
                        height=55, font=("Arial", 18, "bold"), fg_color="#3b8ed0", hover_color="#2d70a7")
    btn_leer.pack(padx=15, pady=15)

    # Configurar el peso de las filas
    ventana.grid_rowconfigure(3, weight=1)

def vista_actualizar():
    ventana = CTkToplevel()
    ventana.geometry("1200x800")
    ventana.title("✏️ Actualizar Unidad Educativa")
    ventana.configure(fg_color="#1e1e1e")
    
    # Configurar el grid principal
    ventana.grid_columnconfigure(1, weight=1)
    
    # Frame para organizar mejor los elementos
    main_frame = CTkFrame(ventana, fg_color="#2e2e2e")
    main_frame.grid(row=0, column=0, columnspan=2, padx=30, pady=30, sticky="nsew")
    main_frame.grid_columnconfigure(1, weight=1)

    # Título
    CTkLabel(main_frame, text="✏️ ACTUALIZAR UNIDAD EDUCATIVA", font=("Arial", 24, "bold")).grid(row=0, column=0, columnspan=2, pady=25)

    # Campo ID obligatorio
    CTkLabel(main_frame, text="🔢 ID de la UE a actualizar:", font=("Arial", 16)).grid(row=1, column=0, padx=15, pady=15, sticky="e")
    entry_id = CTkEntry(main_frame, height=45, font=("Arial", 14))
    entry_id.grid(row=1, column=1, padx=15, pady=15, sticky="ew")

    # Separador
    CTkLabel(main_frame, text="📝 Complete solo los campos a actualizar:", font=("Arial", 16)).grid(row=2, column=0, columnspan=2, pady=20)

    # Campos opcionales para actualización
    campos = {
        "nombre": CTkEntry(main_frame, placeholder_text="🏫 Nuevo nombre", height=45, font=("Arial", 14)),
        "nombre_director": CTkEntry(main_frame, placeholder_text="👨‍💼 Nuevo nombre del director", height=45, font=("Arial", 14)),
        "tipo": CTkOptionMenu(main_frame, values=["", "🏛️ Pública", "💼 Privada", "🏢 Municipal"], height=45, font=("Arial", 14)),
        "telefono": CTkEntry(main_frame, placeholder_text="📞 11 dígitos", height=45, font=("Arial", 14)),
        "direccion": CTkEntry(main_frame, placeholder_text="📍 Nueva dirección", height=45, font=("Arial", 14))
    }

    # Posicionamiento de los campos
    for i, (label_text, entry) in enumerate([
        ("🏫 Nuevo Nombre UE:", campos["nombre"]),
        ("👨‍💼 Nuevo Nombre Director:", campos["nombre_director"]),
        ("🏛️ Nuevo Tipo UE:", campos["tipo"]),
        ("📞 Nuevo Teléfono:", campos["telefono"]),
        ("📍 Nueva Dirección:", campos["direccion"])
    ], start=3):
        CTkLabel(main_frame, text=label_text, font=("Arial", 16)).grid(row=i, column=0, padx=15, pady=15, sticky="e")
        entry.grid(row=i, column=1, padx=15, pady=15, sticky="ew")

    # Frame para el botón
    button_frame = CTkFrame(ventana, fg_color="transparent")
    button_frame.grid(row=1, column=0, columnspan=2, pady=25)

    def ejecutar_actualizar():
        id_ue = entry_id.get()
        if not id_ue:
            mostrar_resultado(ventana, {"error": "❌ Debe ingresar un ID", "status": "error"})
            return
        
        # Validar teléfono si se proporciona
        telefono = campos["telefono"].get()
        if telefono and (len(telefono) != 11 or not telefono.isdigit()):
            mostrar_resultado(ventana, {"error": "❌ El teléfono debe tener exactamente 11 dígitos", "status": "error"})
            return
        
        # Solo enviar campos que tengan contenido
        datos_actualizar = {}
        if campos["nombre"].get(): datos_actualizar["nombre"] = campos["nombre"].get()
        if campos["nombre_director"].get(): datos_actualizar["director"] = campos["nombre_director"].get()
        if campos["tipo"].get(): datos_actualizar["tipo"] = campos["tipo"].get().replace("🏛️ ", "").replace("💼 ", "").replace("🏢 ", "")
        if telefono: datos_actualizar["telefono"] = telefono
        if campos["direccion"].get(): datos_actualizar["direccion"] = campos["direccion"].get()
        
        if not datos_actualizar:
            mostrar_resultado(ventana, {"error": "❌ No hay datos para actualizar", "status": "error"})
            return
            
        resultado = actualizar(id_ue, **datos_actualizar)
        mostrar_resultado(ventana, resultado)

    btn_actualizar = CTkButton(button_frame, text="✏️ ACTUALIZAR", command=ejecutar_actualizar,
                              height=55, font=("Arial", 18, "bold"), fg_color="#f0b400", hover_color="#c79500")
    btn_actualizar.pack(padx=15, pady=15)

def vista_eliminar():
    # Crear ventana para eliminar UE
    ventana = CTkToplevel()
    ventana.geometry("800x500")
    ventana.title("🗑️ Eliminar Unidad Educativa")
    ventana.configure(fg_color="#1e1e1e")

    frame_principal = CTkFrame(ventana, fg_color="#2e2e2e")
    frame_principal.pack(expand=True, fill="both", padx=40, pady=40)

    CTkLabel(frame_principal, text="🗑️ ELIMINAR UNIDAD EDUCATIVA", 
             font=("Arial", 24, "bold")).pack(pady=30)

    CTkLabel(frame_principal, text="🔢 ID de la UE a eliminar:", 
             font=("Arial", 18)).pack(pady=20)
    
    entry_id = CTkEntry(frame_principal, height=50, font=("Arial", 16))
    entry_id.pack(pady=20, padx=50, fill="x")

    def ejecutar_eliminar():
        id_ue = entry_id.get()
        if not id_ue:
            mostrar_resultado(ventana, {"error": "❌ Debe ingresar un ID", "status": "error"})
            return
        
        # Confirmación
        confirmacion = CTkToplevel(ventana)
        confirmacion.title("⚠️ Confirmar Eliminación")
        confirmacion.geometry("500x300")
        confirmacion.configure(fg_color="#1e1e1e")
        
        CTkLabel(confirmacion, text=f"¿Está seguro de eliminar la Unidad Educativa con ID {id_ue}?", 
                font=("Arial", 16), wraplength=400).pack(pady=40)
        
        def confirmar():
            resultado = eliminar(id_ue)
            mostrar_resultado(ventana, resultado)
            confirmacion.destroy()
        
        frame_botones = CTkFrame(confirmacion, fg_color="transparent")
        frame_botones.pack(pady=30)
        
        CTkButton(frame_botones, text="✅ Sí, Eliminar", command=confirmar, 
                 fg_color="#e74c3c", hover_color="#c0392b", height=45, font=("Arial", 16)).pack(side="left", padx=20)
        CTkButton(frame_botones, text="❌ Cancelar", command=confirmacion.destroy,
                 height=45, font=("Arial", 16)).pack(side="right", padx=20)

    btn_eliminar = CTkButton(frame_principal, text="🗑️ ELIMINAR UNIDAD EDUCATIVA", command=ejecutar_eliminar,
                            height=55, font=("Arial", 18, "bold"), fg_color="#e74c3c", hover_color="#c0392b")
    btn_eliminar.pack(pady=30)

if __name__ == "__main__":
    main()