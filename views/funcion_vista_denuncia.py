import customtkinter as ctk
from tkinter import messagebox
from controllers.denuncia_controller import DenunciaController 

# ----------------------------------------------------------------------
# CLASE DE VISTA ADAPTADA (Estructura de ArticuloViewFrame)
# ----------------------------------------------------------------------

class FuncionVistaDenuncia(ctk.CTkFrame):

    def __init__(self, master, controller: DenunciaController):
        super().__init__(master, corner_radius=0, fg_color="transparent") 
        
        self.controller = controller 
        # La Vista se registra en el Controlador para que este pueda actualizarla
        self.controller.set_view(self) 
        
        self.denuncia_id_cargada = None
        
        # Variables de control (adaptadas para un posible formulario de Denuncia)
        self.buscar_var = ctk.StringVar(self) # Para buscar por ID o Título
        self.titulo_var = ctk.StringVar(self) # NOTA: La tabla denuncia NO tiene campo titulo, se usa descripción
        self.denunciante_var = ctk.StringVar(self)
        self.estado_var = ctk.StringVar(self, value="Pendiente") # Por ejemplo, para el estado
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        self._configurar_interfaz() 

    # MÉTODO CLAVE: Requerido por la estructura de la aplicación principal
    def show(self):
        """Llamado por MenuApp, invoca la carga de datos iniciales del controlador."""
        self.controller.load_initial_data() 

    def _configurar_interfaz(self):
        """Configura la interfaz gráfica dentro de este frame."""
        
        # Título y Mensajes (Similar a ArticuloViewFrame)
        self.title_label = ctk.CTkLabel(self, text="🚨 GESTIÓN DE DENUNCIAS LOPNNA", 
                                        font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="ew")

        # Mensaje de estado (en la fila 1)
        self.message_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14), text_color="yellow")
        self.message_label.grid(row=1, column=0, pady=5, padx=20, sticky="ew")

        # Contenedor principal de formulario y búsqueda (en la fila 2)
        content_frame = ctk.CTkFrame(self, fg_color="#111111", corner_radius=10)
        content_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        content_frame.columnconfigure(0, weight=1)

        # 1. Frame de Búsqueda (Similar a ArticuloViewFrame)
        search_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        search_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        search_frame.columnconfigure(0, weight=1)
        
        ctk.CTkLabel(search_frame, text="Buscar Denuncia (ID o Título)", font=("Arial", 14)).grid(row=0, column=0, sticky="w", padx=10, pady=(0, 5))
        
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.buscar_var, placeholder_text="Ingrese ID o Título...", height=40)
        search_entry.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        ctk.CTkButton(search_frame, text="🔍 Buscar", command=self._handle_buscar_denuncia, height=40,
                      fg_color="#3498db", hover_color="#2980b9").grid(row=1, column=1, padx=(10, 0), pady=(0, 10))

        # Separador
        ctk.CTkFrame(content_frame, height=2, fg_color="#555555").grid(row=1, column=0, sticky="ew", padx=20)
        
        # 2. Frame de Formulario (Adaptado de ArticuloViewFrame)
        form_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        form_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        form_frame.columnconfigure((0, 1), weight=1)
        
        # Campos del Formulario (Ejemplo: Título, Denunciante, Estado)
        fields = [
            # NOTA: En la DB el título se extrae de la descripción, pero lo mantenemos para el input
            ("Título de Denuncia (Resumen)", self.titulo_var), 
            ("Denunciante (Solo Referencia)", self.denunciante_var),
        ]
        
        for i, (label_text, var) in enumerate(fields):
            ctk.CTkLabel(form_frame, text=label_text, font=("Arial", 14)).grid(row=i, column=0, sticky="w", padx=10, pady=(10, 5))
            ctk.CTkEntry(form_frame, textvariable=var, height=40, font=("Arial", 14)).grid(row=i, column=1, sticky="ew", padx=10, pady=(10, 5))

        # Campo de Estado (Usando OptionMenu)
        row_idx = len(fields)
        ctk.CTkLabel(form_frame, text="Estado", font=("Arial", 14)).grid(row=row_idx, column=0, sticky="w", padx=10, pady=(10, 5))
        estados = ["Pendiente", "En Revisión", "Resuelto", "Rechazado"]
        self.estado_menu = ctk.CTkOptionMenu(form_frame, variable=self.estado_var, values=estados, height=40)
        self.estado_menu.grid(row=row_idx, column=1, sticky="ew", padx=10, pady=(10, 5))
        
        # Campo de Descripción (ocupa 2 columnas, altura ajustada)
        row_idx += 1
        ctk.CTkLabel(form_frame, text="Descripción/Detalles", font=("Arial", 14)).grid(row=row_idx, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))
        self.desc_textbox = ctk.CTkTextbox(form_frame, height=180, font=("Arial", 14)) # Mayor altura para la descripción
        self.desc_textbox.grid(row=row_idx + 1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))

        # 3. Frame de Botones (Similar a ArticuloViewFrame)
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        # Botones
        ctk.CTkButton(button_frame, text="➕ Crear", command=self._handle_crear_denuncia, height=45, 
                      fg_color="#2ecc71", hover_color="#27ae60", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", expand=True, fill="x", padx=5)
        
        self.btn_modificar = ctk.CTkButton(button_frame, text="✏️ Modificar", command=self._handle_modificar_denuncia, height=45, 
                      fg_color="#f39c12", hover_color="#e67e22", font=ctk.CTkFont(size=16, weight="bold"), state="disabled")
        self.btn_modificar.pack(side="left", expand=True, fill="x", padx=5)
        
        self.btn_eliminar = ctk.CTkButton(button_frame, text="🗑️ Eliminar", command=self._handle_eliminar_denuncia, height=45, 
                      fg_color="#e74c3c", hover_color="#c0392b", font=ctk.CTkFont(size=16, weight="bold"), state="disabled")
        self.btn_eliminar.pack(side="left", expand=True, fill="x", padx=5)
        
        ctk.CTkButton(button_frame, text="🧹 Limpiar", command=self.limpiar_entradas, height=45, 
                      fg_color="#95a5a6", hover_color="#7f8c8d", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", expand=True, fill="x", padx=5)

    # ----------------------------------------------------------------------
    # Métodos de Eventos (Delegación al Controlador - Adaptados)
    # ----------------------------------------------------------------------
    
    def _handle_crear_denuncia(self):
        # NOTA: En un sistema real, se requeriría un formulario adicional 
        # para obtener los datos completos (consejero_id, fecha_hechos, denunciantes, NNA, etc.)
        data = self._obtener_datos_formulario() 
        self.controller.handle_crear_denuncia(data["titulo"], data["denunciante"], data["estado"], data["descripcion"])
            
    def _handle_buscar_denuncia(self):
        termino = self.buscar_var.get()
        self.controller.handle_buscar_denuncia(termino)
            
    def _handle_modificar_denuncia(self):
        if not self.denuncia_id_cargada:
            self.display_message("❌ Primero debe buscar y cargar una denuncia para modificarla.", is_success=False)
            return

        # NOTA: Solo se modificará la descripción y el estado principal en esta vista simplificada.
        data = self._obtener_datos_formulario()
        self.controller.handle_modificar_denuncia(self.denuncia_id_cargada, 
                                                  data["titulo"], data["denunciante"], 
                                                  data["estado"], data["descripcion"])
            
    def _handle_eliminar_denuncia(self):
        if not self.denuncia_id_cargada:
            self.display_message("❌ Primero debe buscar y cargar una denuncia para eliminarla.", is_success=False)
            return
            
        if messagebox.askyesno("⚠️ Confirmación", "¿Está seguro de que desea eliminar esta denuncia?"):
            self.controller.handle_eliminar_denuncia(self.denuncia_id_cargada)
    
    # ----------------------------------------------------------------------
    # Métodos de Mutación de Vista (Llamados por el Controlador - Adaptados)
    # ----------------------------------------------------------------------

    def limpiar_entradas(self): 
        """Limpia todos los campos del formulario."""
        self.buscar_var.set("")
        self.titulo_var.set("")
        self.denunciante_var.set("")
        self.estado_var.set("Pendiente") 
        self.desc_textbox.delete("1.0", "end")
        self.denuncia_id_cargada = None
        self._set_btn_state("disabled")
        self.display_message("")

    def _obtener_datos_formulario(self): 
        """Recolecta los datos de los campos de entrada."""
        return {
            "titulo": self.titulo_var.get(), # Se mantiene el campo aunque no vaya directo a DB
            "denunciante": self.denunciante_var.get(),
            "estado": self.estado_var.get(),
            "descripcion": self.desc_textbox.get("1.0", "end-1c").strip()
        }
        
    def _establecer_datos_formulario(self, data: dict): 
        """Establece los valores en los campos de entrada y habilita botones."""
        # 'titulo' viene de la sub-string de descripción generada en el modelo para la lista
        self.titulo_var.set(data.get("titulo", "")) 
        # 'denunciante' NO es un campo directo de la DB denuncia, se asume un campo simulado
        self.denunciante_var.set(data.get("denunciante", "No disponible")) 
        
        # Mapeo del estado booleano de la DB a string de la vista
        estado_db = data.get("estado")
        estado_str = "Pendiente" if estado_db is True else "Resuelto" if estado_db is False else data.get("estado_str", "Pendiente")
        self.estado_var.set(estado_str) 
        
        # La descripción es la principal data
        self.desc_textbox.delete("1.0", "end")
        self.desc_textbox.insert("1.0", data.get("descripcion", ""))
        self.denuncia_id_cargada = data.get("id")
        self._set_btn_state("normal")
        
    def _set_btn_state(self, state):
        """Habilita o deshabilita los botones de Modificar/Eliminar."""
        self.btn_modificar.configure(state=state)
        self.btn_eliminar.configure(state=state)
        
    def display_message(self, message: str, is_success: bool = True):
        """Muestra un mensaje de estado en la interfaz (Similar a ArticuloViewFrame)."""
        color = "#2ecc71" if is_success else "#e74c3c"
        self.message_label.configure(text=message, text_color=color)