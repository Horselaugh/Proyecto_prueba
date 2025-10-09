from customtkinter import *
from modulo_gestion_matricula import crear, leer, actualizar, eliminar

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
    ventana.title("Gestión de Matrículas Educativas")
    ventana.configure(fg_color="#2e2e2e")

    # Botones de acción
    btn_crear = CTkButton(ventana, text="Crear Matrícula", command=vista_crear)
    btn_crear.pack(pady=10)
    
    btn_leer = CTkButton(ventana, text="Buscar Matrícula", command=vista_leer)
    btn_leer.pack(pady=10)

    btn_actualizar = CTkButton(ventana, text="Actualizar Matrícula", command=vista_actualizar)
    btn_actualizar.pack(pady=10)

    btn_eliminar = CTkButton(ventana, text="Eliminar Matrícula", command=vista_eliminar)
    btn_eliminar.pack(pady=10)

    ventana.mainloop()

def vista_crear():
    # Crear ventana para crear Matrícula
    ventana = CTkToplevel()
    ventana.geometry("500x400")
    ventana.title("Crear Matrícula Educativa")
    ventana.configure(fg_color="#2e2e2e")
    
    # Configurar grid
    ventana.grid_columnconfigure(1, weight=1)

    # Campos de entrada para Matrícula
    campos = {
        "grado": CTkOptionMenu(ventana, values=["1ro", "2do", "3ro", "4to", "5to", "6to", "7mo", "8vo", "9no", "10mo"]),
        "fecha_matricula": CTkEntry(ventana, placeholder_text="YYYY-MM-DD"),
        "activa": CTkOptionMenu(ventana, values=["Sí", "No"])
    }

    # Posicionamiento
    for i, (label_text, entry) in enumerate([
        ("Grado:", campos["grado"]),
        ("Fecha Matrícula (YYYY-MM-DD):", campos["fecha_matricula"]),
        ("¿Activa?:", campos["activa"])
    ]):
        CTkLabel(ventana, text=label_text).grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")

    def ejecutar_crear():
        # Validar fecha antes de enviar
        fecha = campos["fecha_matricula"].get()
        # Validación básica de formato de fecha (puedes mejorarla)
        if not fecha or len(fecha) != 10 or fecha[4] != '-' or fecha[7] != '-':
            mostrar_resultado(ventana, {"error": "Formato de fecha debe ser YYYY-MM-DD", "status": "error"})
            return
            
        # Convertir "Sí"/"No" a valor booleano/entero para la base de datos
        activa_bool = 1 if campos["activa"].get() == "Sí" else 0
        
        resultado = crear(
            campos["grado"].get(),
            fecha,
            activa_bool
        )
        mostrar_resultado(ventana, resultado)

    btn_crear = CTkButton(ventana, text="CREAR MATRÍCULA", command=ejecutar_crear)
    btn_crear.grid(row=3, column=0, columnspan=2, pady=20)

    ventana.grid_columnconfigure(1, weight=1)

def vista_leer():
    ventana = CTkToplevel()
    ventana.geometry("600x400")
    ventana.title("Buscar Matrícula")
    ventana.configure(fg_color="#2e2e2e")
    ventana.grid_columnconfigure(0, weight=1)

    # Opciones de búsqueda
    CTkLabel(ventana, text="Buscar por:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    
    opcion_busqueda = StringVar(value="grado_fecha")
    frame_opciones = CTkFrame(ventana)
    frame_opciones.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
    
    CTkRadioButton(frame_opciones, text="Grado y Fecha", variable=opcion_busqueda, value="grado_fecha").pack(side="left", padx=10)
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
        
        if opcion_busqueda.get() == "grado_fecha":
            # Campos para grado y fecha
            CTkLabel(frame_campos, text="Grado:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
            entry_grado = CTkOptionMenu(frame_campos, values=["1ro", "2do", "3ro", "4to", "5to", "6to", "7mo", "8vo", "9no", "10mo"])
            entry_grado.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            
            CTkLabel(frame_campos, text="Fecha (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
            entry_fecha = CTkEntry(frame_campos, placeholder_text="YYYY-MM-DD")
            entry_fecha.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
            
            current_entries["grado"] = entry_grado
            current_entries["fecha_matricula"] = entry_fecha
        else:
            # Campo para ID
            CTkLabel(frame_campos, text="ID Matrícula:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
            entry_id = CTkEntry(frame_campos)
            entry_id.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            
            current_entries["id"] = entry_id
    
    # Configurar el trace
    opcion_busqueda.trace_add("write", lambda *args: mostrar_campos())
    
    # Mostrar campos iniciales
    mostrar_campos()

    def ejecutar_leer():
        if opcion_busqueda.get() == "grado_fecha":
            grado = current_entries["grado"].get() if "grado" in current_entries else ""
            fecha = current_entries["fecha_matricula"].get() if "fecha_matricula" in current_entries else ""
            if not grado or not fecha:
                mostrar_resultado(ventana, {"error": "Debe ingresar grado y fecha", "status": "error"})
                return
            resultado = leer(grado=grado, fecha_matricula=fecha)
        else:
            id_matricula = current_entries["id"].get() if "id" in current_entries else ""
            if not id_matricula:
                mostrar_resultado(ventana, {"error": "Debe ingresar un ID", "status": "error"})
                return
            resultado = leer(id=id_matricula)
        
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
    ventana.geometry("500x400")
    ventana.title("Actualizar Matrícula")
    ventana.configure(fg_color="#2e2e2e")
    
    # Configurar el grid principal
    ventana.grid_columnconfigure(1, weight=1)
    
    # Frame para organizar mejor los elementos
    main_frame = CTkFrame(ventana)
    main_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    main_frame.grid_columnconfigure(1, weight=1)

    # Campo ID obligatorio
    CTkLabel(main_frame, text="ID de la Matrícula a actualizar:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_id = CTkEntry(main_frame)
    entry_id.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    # Separador
    CTkLabel(main_frame, text="Complete solo los campos a actualizar:").grid(row=1, column=0, columnspan=2, pady=10)

    # Campos opcionales para actualización
    campos = {
        "grado": CTkOptionMenu(main_frame, values=["", "1ro", "2do", "3ro", "4to", "5to", "6to", "7mo", "8vo", "9no", "10mo"]),
        "fecha_matricula": CTkEntry(main_frame, placeholder_text="YYYY-MM-DD"),
        "activa": CTkOptionMenu(main_frame, values=["", "Sí", "No"])
    }

    # Posicionamiento de los campos
    for i, (label_text, entry) in enumerate([
        ("Nuevo Grado:", campos["grado"]),
        ("Nueva Fecha (YYYY-MM-DD):", campos["fecha_matricula"]),
        ("Nuevo Estado Activa:", campos["activa"])
    ], start=2):
        CTkLabel(main_frame, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky="e")
        entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")

    # Frame para el botón
    button_frame = CTkFrame(ventana)
    button_frame.grid(row=1, column=0, columnspan=2, pady=10)
    button_frame.grid_columnconfigure(0, weight=1)

    def ejecutar_actualizar():
        id_matricula = entry_id.get()
        if not id_matricula:
            mostrar_resultado(ventana, {"error": "Debe ingresar un ID", "status": "error"})
            return
        
        # Validar fecha si se proporciona
        fecha = campos["fecha_matricula"].get()
        if fecha and (len(fecha) != 10 or fecha[4] != '-' or fecha[7] != '-'):
            mostrar_resultado(ventana, {"error": "Formato de fecha debe ser YYYY-MM-DD", "status": "error"})
            return
        
        # Solo enviar campos que tengan contenido
        datos_actualizar = {}
        if campos["grado"].get(): datos_actualizar["grado"] = campos["grado"].get()
        if fecha: datos_actualizar["fecha_matricula"] = fecha
        if campos["activa"].get(): 
            datos_actualizar["activa"] = 1 if campos["activa"].get() == "Sí" else 0
        
        if not datos_actualizar:
            mostrar_resultado(ventana, {"error": "No hay datos para actualizar", "status": "error"})
            return
            
        resultado = actualizar(id_matricula, **datos_actualizar)
        mostrar_resultado(ventana, resultado)

    btn_actualizar = CTkButton(button_frame, text="ACTUALIZAR", command=ejecutar_actualizar)
    btn_actualizar.grid(row=0, column=0, padx=10, pady=5)

def vista_eliminar():
    # Crear ventana para eliminar Matrícula
    ventana = CTkToplevel()
    ventana.geometry("400x200")
    ventana.title("Eliminar Matrícula")
    ventana.configure(fg_color="#2e2e2e")

    CTkLabel(ventana, text="ID de la Matrícula a eliminar:").pack(pady=10)
    entry_id = CTkEntry(ventana)
    entry_id.pack(pady=10)

    def ejecutar_eliminar():
        id_matricula = entry_id.get()
        if not id_matricula:
            mostrar_resultado(ventana, {"error": "Debe ingresar un ID", "status": "error"})
            return
        
        # Confirmación
        confirmacion = CTkToplevel(ventana)
        confirmacion.title("Confirmar Eliminación")
        confirmacion.geometry("300x150")
        
        CTkLabel(confirmacion, text=f"¿Eliminar Matrícula con ID {id_matricula}?").pack(pady=20)
        
        def confirmar():
            resultado = eliminar(id_matricula)
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