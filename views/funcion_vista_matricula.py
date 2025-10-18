# funcion_vista_matricula.py
from customtkinter import *
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controllers.matricula_controller import crear, leer, actualizar, eliminar

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
    ventana.title("🎓 Gestión de Matrículas Educativas")
    ventana.configure(fg_color="#1e1e1e")

    # Centrar contenido
    frame_principal = CTkFrame(ventana, fg_color="transparent")
    frame_principal.pack(expand=True, fill="both", padx=80, pady=80)
    
    CTkLabel(frame_principal, text="🎓 GESTIÓN DE MATRÍCULAS EDUCATIVAS", 
             font=("Arial", 28, "bold")).pack(pady=40)
    
    CTkLabel(frame_principal, text="Seleccione una operación:", 
             font=("Arial", 18)).pack(pady=30)

    # Frame para botones
    frame_botones = CTkFrame(frame_principal, fg_color="transparent")
    frame_botones.pack(expand=True, pady=40)

    btn_crear = CTkButton(frame_botones, text="➕ CREAR MATRÍCULA", 
                         command=vista_crear, height=60, width=300,
                         font=("Arial", 18, "bold"), fg_color="#2aa876", hover_color="#228c61")
    btn_crear.pack(pady=20)
    
    btn_leer = CTkButton(frame_botones, text="🔍 BUSCAR MATRÍCULA", 
                        command=vista_leer, height=60, width=300,
                        font=("Arial", 18, "bold"), fg_color="#3b8ed0", hover_color="#2d70a7")
    btn_leer.pack(pady=20)

    btn_actualizar = CTkButton(frame_botones, text="✏️ ACTUALIZAR MATRÍCULA", 
                              command=vista_actualizar, height=60, width=300,
                              font=("Arial", 18, "bold"), fg_color="#f0b400", hover_color="#c79500")
    btn_actualizar.pack(pady=20)

    btn_eliminar = CTkButton(frame_botones, text="🗑️ ELIMINAR MATRÍCULA", 
                            command=vista_eliminar, height=60, width=300,
                            font=("Arial", 18, "bold"), fg_color="#e74c3c", hover_color="#c0392b")
    btn_eliminar.pack(pady=20)

    ventana.mainloop()

def vista_crear():
    ventana = CTkToplevel()
    ventana.geometry("1200x800")
    ventana.title("➕ Crear Matrícula Educativa")
    ventana.configure(fg_color="#1e1e1e")
    ventana.grid_columnconfigure(1, weight=1)

    # Título
    CTkLabel(ventana, text="➕ CREAR NUEVA MATRÍCULA", 
             font=("Arial", 24, "bold")).grid(row=0, column=0, columnspan=2, pady=30)

    campos = {
        "nna_id": CTkEntry(ventana, placeholder_text="🔢 Ingrese ID del NNA", height=45, font=("Arial", 14)),
        "unidad_id": CTkEntry(ventana, placeholder_text="🏫 Ingrese ID de la Unidad Educativa", height=45, font=("Arial", 14)),
        "grado": CTkOptionMenu(ventana, values=["1ro", "2do", "3ro", "4to", "5to", "6to", "7mo", "8vo", "9no", "10mo"], height=45, font=("Arial", 14)),
        "fecha_matricula": CTkEntry(ventana, placeholder_text="📅 YYYY-MM-DD", height=45, font=("Arial", 14)),
        "activa": CTkOptionMenu(ventana, values=["✅ Sí", "❌ No"], height=45, font=("Arial", 14))
    }

    labels = [
        ("🔢 ID del NNA*:", campos["nna_id"]),
        ("🏫 ID de la Unidad Educativa*:", campos["unidad_id"]),
        ("📚 Grado:", campos["grado"]),
        ("📅 Fecha Matrícula:", campos["fecha_matricula"]),
        ("🔄 ¿Activa?:", campos["activa"])
    ]

    for i, (label_text, entry) in enumerate(labels, start=1):
        CTkLabel(ventana, text=label_text, font=("Arial", 16)).grid(row=i, column=0, padx=30, pady=15, sticky="e")
        entry.grid(row=i, column=1, padx=30, pady=15, sticky="ew")

    def ejecutar_crear():
        nna_id = campos["nna_id"].get()
        unidad_id = campos["unidad_id"].get()
        
        if not nna_id or not unidad_id:
            mostrar_resultado(ventana, {"error": "❌ ID del NNA y Unidad Educativa son obligatorios", "status": "error"})
            return
            
        fecha = campos["fecha_matricula"].get()
        if fecha and (len(fecha) != 10 or fecha[4] != '-' or fecha[7] != '-'):
            mostrar_resultado(ventana, {"error": "❌ Formato de fecha debe ser YYYY-MM-DD", "status": "error"})
            return
            
        activa_bool = True if campos["activa"].get() == "✅ Sí" else False
        
        resultado = crear(
            nna_id=int(nna_id),
            unidad_id=int(unidad_id),
            grado=campos["grado"].get(),
            fecha_matricula=fecha or None,
            activa=activa_bool
        )
        mostrar_resultado(ventana, resultado)

    btn_crear = CTkButton(ventana, text="🚀 CREAR MATRÍCULA", command=ejecutar_crear,
                         height=55, font=("Arial", 18, "bold"), fg_color="#2aa876", hover_color="#228c61")
    btn_crear.grid(row=6, column=0, columnspan=2, pady=40)

def vista_leer():
    ventana = CTkToplevel()
    ventana.geometry("1200x800")
    ventana.title("🔍 Buscar Matrícula")
    ventana.configure(fg_color="#1e1e1e")
    ventana.grid_columnconfigure(0, weight=1)

    CTkLabel(ventana, text="🔍 BUSCAR MATRÍCULA", font=("Arial", 24, "bold")).grid(row=0, column=0, pady=30)
    
    CTkLabel(ventana, text="🔎 Buscar por:", font=("Arial", 18)).grid(row=1, column=0, sticky="w", padx=30, pady=15)
    
    opcion_busqueda = StringVar(value="nna")
    frame_opciones = CTkFrame(ventana, fg_color="#2e2e2e")
    frame_opciones.grid(row=2, column=0, sticky="ew", padx=30, pady=15)
    
    CTkRadioButton(frame_opciones, text="👦 Por NNA", variable=opcion_busqueda, value="nna", font=("Arial", 16)).pack(side="left", padx=25, pady=10)
    CTkRadioButton(frame_opciones, text="🏫 Por Unidad", variable=opcion_busqueda, value="unidad", font=("Arial", 16)).pack(side="left", padx=25, pady=10)
    CTkRadioButton(frame_opciones, text="🔗 Por ambos", variable=opcion_busqueda, value="ambos", font=("Arial", 16)).pack(side="left", padx=25, pady=10)

    frame_campos = CTkFrame(ventana, fg_color="#2e2e2e")
    frame_campos.grid(row=3, column=0, sticky="nsew", padx=30, pady=25)
    frame_campos.grid_columnconfigure(1, weight=1)

    current_entries = {}
    
    def mostrar_campos():
        for widget in frame_campos.winfo_children():
            widget.destroy()
        
        if opcion_busqueda.get() == "nna":
            CTkLabel(frame_campos, text="👦 ID del NNA:", font=("Arial", 16)).grid(row=0, column=0, padx=15, pady=20, sticky="e")
            entry_nna = CTkEntry(frame_campos, height=45, font=("Arial", 14))
            entry_nna.grid(row=0, column=1, padx=15, pady=20, sticky="ew")
            current_entries["nna_id"] = entry_nna
            
        elif opcion_busqueda.get() == "unidad":
            CTkLabel(frame_campos, text="🏫 ID de la Unidad:", font=("Arial", 16)).grid(row=0, column=0, padx=15, pady=20, sticky="e")
            entry_unidad = CTkEntry(frame_campos, height=45, font=("Arial", 14))
            entry_unidad.grid(row=0, column=1, padx=15, pady=20, sticky="ew")
            current_entries["unidad_id"] = entry_unidad
            
        else:  # ambos
            CTkLabel(frame_campos, text="👦 ID del NNA:", font=("Arial", 16)).grid(row=0, column=0, padx=15, pady=20, sticky="e")
            entry_nna = CTkEntry(frame_campos, height=45, font=("Arial", 14))
            entry_nna.grid(row=0, column=1, padx=15, pady=20, sticky="ew")
            
            CTkLabel(frame_campos, text="🏫 ID de la Unidad:", font=("Arial", 16)).grid(row=1, column=0, padx=15, pady=20, sticky="e")
            entry_unidad = CTkEntry(frame_campos, height=45, font=("Arial", 14))
            entry_unidad.grid(row=1, column=1, padx=15, pady=20, sticky="ew")
            
            current_entries["nna_id"] = entry_nna
            current_entries["unidad_id"] = entry_unidad
    
    opcion_busqueda.trace_add("write", lambda *args: mostrar_campos())
    mostrar_campos()

    def ejecutar_leer():
        if opcion_busqueda.get() == "nna":
            nna_id = current_entries["nna_id"].get() if "nna_id" in current_entries else ""
            if not nna_id:
                mostrar_resultado(ventana, {"error": "❌ Debe ingresar ID del NNA", "status": "error"})
                return
            resultado = leer(nna_id=int(nna_id))
            
        elif opcion_busqueda.get() == "unidad":
            unidad_id = current_entries["unidad_id"].get() if "unidad_id" in current_entries else ""
            if not unidad_id:
                mostrar_resultado(ventana, {"error": "❌ Debe ingresar ID de la unidad", "status": "error"})
                return
            resultado = leer(unidad_id=int(unidad_id))
            
        else:  # ambos
            nna_id = current_entries["nna_id"].get() if "nna_id" in current_entries else ""
            unidad_id = current_entries["unidad_id"].get() if "unidad_id" in current_entries else ""
            if not nna_id or not unidad_id:
                mostrar_resultado(ventana, {"error": "❌ Debe ingresar ambos IDs", "status": "error"})
                return
            resultado = leer(nna_id=int(nna_id), unidad_id=int(unidad_id))
        
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
    ventana.title("✏️ Actualizar Matrícula")
    ventana.configure(fg_color="#1e1e1e")
    ventana.grid_columnconfigure(1, weight=1)
    
    main_frame = CTkFrame(ventana, fg_color="#2e2e2e")
    main_frame.grid(row=0, column=0, columnspan=2, padx=30, pady=30, sticky="nsew")
    main_frame.grid_columnconfigure(1, weight=1)

    CTkLabel(main_frame, text="✏️ ACTUALIZAR MATRÍCULA", font=("Arial", 24, "bold")).grid(row=0, column=0, columnspan=2, pady=25)

    CTkLabel(main_frame, text="🔢 ID de la Matrícula a actualizar:", font=("Arial", 16)).grid(row=1, column=0, padx=15, pady=15, sticky="e")
    entry_id = CTkEntry(main_frame, height=45, font=("Arial", 14))
    entry_id.grid(row=1, column=1, padx=15, pady=15, sticky="ew")

    CTkLabel(main_frame, text="📝 Complete solo los campos a actualizar:", font=("Arial", 16)).grid(row=2, column=0, columnspan=2, pady=20)

    campos = {
        "nna_id": CTkEntry(main_frame, placeholder_text="👦 Nuevo ID del NNA", height=45, font=("Arial", 14)),
        "unidad_id": CTkEntry(main_frame, placeholder_text="🏫 Nuevo ID de la Unidad", height=45, font=("Arial", 14)),
        "grado": CTkOptionMenu(main_frame, values=["", "1ro", "2do", "3ro", "4to", "5to", "6to", "7mo", "8vo", "9no", "10mo"], height=45, font=("Arial", 14)),
        "fecha_matricula": CTkEntry(main_frame, placeholder_text="📅 YYYY-MM-DD", height=45, font=("Arial", 14)),
        "activa": CTkOptionMenu(main_frame, values=["", "✅ Sí", "❌ No"], height=45, font=("Arial", 14))
    }

    labels = [
        ("👦 Nuevo ID del NNA:", campos["nna_id"]),
        ("🏫 Nuevo ID de la Unidad:", campos["unidad_id"]),
        ("📚 Nuevo Grado:", campos["grado"]),
        ("📅 Nueva Fecha Matrícula:", campos["fecha_matricula"]),
        ("🔄 Nuevo Estado Activa:", campos["activa"])
    ]

    for i, (label_text, entry) in enumerate(labels, start=3):
        CTkLabel(main_frame, text=label_text, font=("Arial", 16)).grid(row=i, column=0, padx=15, pady=15, sticky="e")
        entry.grid(row=i, column=1, padx=15, pady=15, sticky="ew")

    def ejecutar_actualizar():
        id_matricula = entry_id.get()
        if not id_matricula:
            mostrar_resultado(ventana, {"error": "❌ Debe ingresar un ID de matrícula", "status": "error"})
            return
        
        datos_actualizar = {}
        if campos["nna_id"].get(): 
            datos_actualizar["nna_id"] = int(campos["nna_id"].get())
        if campos["unidad_id"].get(): 
            datos_actualizar["unidad_id"] = int(campos["unidad_id"].get())
        if campos["grado"].get(): 
            datos_actualizar["grado"] = campos["grado"].get()
        if campos["fecha_matricula"].get(): 
            fecha = campos["fecha_matricula"].get()
            if len(fecha) != 10 or fecha[4] != '-' or fecha[7] != '-':
                mostrar_resultado(ventana, {"error": "❌ Formato de fecha debe ser YYYY-MM-DD", "status": "error"})
                return
            datos_actualizar["fecha_matricula"] = fecha
        if campos["activa"].get(): 
            datos_actualizar["activa"] = True if campos["activa"].get() == "✅ Sí" else False
        
        if not datos_actualizar:
            mostrar_resultado(ventana, {"error": "❌ No hay datos para actualizar", "status": "error"})
            return
            
        resultado = actualizar(id_matricula, **datos_actualizar)
        mostrar_resultado(ventana, resultado)

    button_frame = CTkFrame(ventana, fg_color="transparent")
    button_frame.grid(row=1, column=0, columnspan=2, pady=25)
    btn_actualizar = CTkButton(button_frame, text="✏️ ACTUALIZAR", command=ejecutar_actualizar,
                              height=55, font=("Arial", 18, "bold"), fg_color="#f0b400", hover_color="#c79500")
    btn_actualizar.pack(padx=15, pady=15)

def vista_eliminar():
    ventana = CTkToplevel()
    ventana.geometry("800x500")
    ventana.title("🗑️ Eliminar Matrícula")
    ventana.configure(fg_color="#1e1e1e")

    frame_principal = CTkFrame(ventana, fg_color="#2e2e2e")
    frame_principal.pack(expand=True, fill="both", padx=40, pady=40)

    CTkLabel(frame_principal, text="🗑️ ELIMINAR MATRÍCULA", 
             font=("Arial", 24, "bold")).pack(pady=30)

    CTkLabel(frame_principal, text="🔢 ID de la Matrícula a eliminar:", 
             font=("Arial", 18)).pack(pady=20)
    
    entry_id = CTkEntry(frame_principal, height=50, font=("Arial", 16))
    entry_id.pack(pady=20, padx=50, fill="x")

    def ejecutar_eliminar():
        id_matricula = entry_id.get()
        if not id_matricula:
            mostrar_resultado(ventana, {"error": "❌ Debe ingresar un ID de matrícula", "status": "error"})
            return
        
        confirmacion = CTkToplevel(ventana)
        confirmacion.title("⚠️ Confirmar Eliminación")
        confirmacion.geometry("500x300")
        confirmacion.configure(fg_color="#1e1e1e")
        
        CTkLabel(confirmacion, text=f"¿Está seguro de eliminar la matrícula con ID {id_matricula}?", 
                font=("Arial", 16), wraplength=400).pack(pady=40)
        
        def confirmar():
            resultado = eliminar(id_matricula)
            mostrar_resultado(ventana, resultado)
            confirmacion.destroy()
        
        frame_botones = CTkFrame(confirmacion, fg_color="transparent")
        frame_botones.pack(pady=30)
        
        CTkButton(frame_botones, text="✅ Sí, Eliminar", command=confirmar, 
                 fg_color="#e74c3c", hover_color="#c0392b", height=45, font=("Arial", 16)).pack(side="left", padx=20)
        CTkButton(frame_botones, text="❌ Cancelar", command=confirmacion.destroy,
                 height=45, font=("Arial", 16)).pack(side="right", padx=20)

    btn_eliminar = CTkButton(frame_principal, text="🗑️ ELIMINAR MATRÍCULA", command=ejecutar_eliminar,
                            height=55, font=("Arial", 18, "bold"), fg_color="#e74c3c", hover_color="#c0392b")
    btn_eliminar.pack(pady=30)

if __name__ == "__main__":
    main()