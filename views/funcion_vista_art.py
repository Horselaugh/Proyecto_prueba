import customtkinter as ctk
from tkinter import messagebox
from controllers.articulo_controller import ArticuloControlador 

    
class ArticuloControlador:
    def __init__(self):
        self.modelo = ArticuloControlador() 
        self.vista = None

    def set_view(self, view_instance):
        self.vista = view_instance
        
    def load_initial_data(self):
        self.vista.display_message("Listo para gestionar Artículos LOPNNA. Use el campo de búsqueda para empezar. 🔎", is_success=True)

    # Delegación de manejo de eventos al controlador (métodos dummy para el mock)
    def handle_crear_articulo(self, *args): self.vista.display_message("Mock: Crear artículo", True)
    def handle_buscar_articulo(self, termino): 
        resultado = self.modelo.buscar_articulo(termino)
        if resultado:
            self.vista._establecer_datos_formulario(resultado)
        else:
            self.vista.display_message("Mock: Artículo no encontrado", False)
            self.vista.limpiar_entradas()
    def handle_modificar_articulo(self, *args): self.vista.display_message("Mock: Modificar artículo", True)
    def handle_eliminar_articulo(self, *args): self.vista.display_message("Mock: Eliminar artículo", True)


# ----------------------------------------------------------------------
# CLASE DE VISTA ADAPTADA
# ----------------------------------------------------------------------

class ArticuloViewFrame(ctk.CTkFrame):
    """
    Vista para el módulo de gestión de Artículos LOPNNA. 
    Hereda de CTkFrame para ser cargado en el panel de contenido de MenuApp.
    """
    
    # MODIFICACIÓN CLAVE: Recibir el master y el controller
    def __init__(self, master, controller: ArticuloControlador):
        super().__init__(master, corner_radius=0, fg_color="transparent") 
        
        self.controller = controller 
        # La Vista se registra en el Controlador para que este pueda actualizarla
        self.controller.set_view(self) 
        
        self.articulo_id_cargado = None
        
        # Variables de control
        self.buscar_var = ctk.StringVar(self)
        self.codigo_var = ctk.StringVar(self)
        self.articulo_var = ctk.StringVar(self)
        self.descripcion_var = ctk.StringVar(self)
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        self._configurar_interfaz() # Renombrado de crear_interfaz a _configurar_interfaz

    # MÉTODO CLAVE: Requerido por la estructura de menu.py
    def show(self):
        """Llamado por MenuApp, invoca la carga de datos iniciales del controlador."""
        self.controller.load_initial_data() 

    def _configurar_interfaz(self):
        """Configura la interfaz gráfica dentro de este frame."""
        
        # Título y Mensajes
        self.title_label = ctk.CTkLabel(self, text="📦 GESTIÓN DE ARTÍCULOS LOPNNA", 
                                        font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="ew")

        self.message_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14), text_color="yellow")
        self.message_label.grid(row=1, column=0, pady=5, padx=20, sticky="ew")

        # Contenedor principal de formulario y búsqueda
        content_frame = ctk.CTkFrame(self, fg_color="#111111", corner_radius=10)
        content_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        content_frame.columnconfigure(0, weight=1)

        # Frame de Búsqueda
        search_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        search_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        search_frame.columnconfigure(0, weight=1)
        
        ctk.CTkLabel(search_frame, text="Buscar Artículo (Código)", font=("Arial", 14)).grid(row=0, column=0, sticky="w", padx=10, pady=(0, 5))
        
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.buscar_var, placeholder_text="Ingrese Código...", height=40)
        search_entry.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        # DELEGACIÓN: El botón llama a un método de la vista que invoca al controlador
        ctk.CTkButton(search_frame, text="🔍 Buscar", command=self._handle_buscar_articulo, height=40,
                      fg_color="#3498db", hover_color="#2980b9").grid(row=1, column=1, padx=(10, 0), pady=(0, 10))

        # Separador
        ctk.CTkFrame(content_frame, height=2, fg_color="#555555").grid(row=1, column=0, sticky="ew", padx=20)
        
        # Frame de Formulario
        form_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        form_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        form_frame.columnconfigure((0, 1), weight=1)
        
        # Campos del Formulario
        fields = [
            ("Código", self.codigo_var),
            ("Artículo/Título", self.articulo_var),
        ]
        
        for i, (label_text, var) in enumerate(fields):
            ctk.CTkLabel(form_frame, text=label_text, font=("Arial", 14)).grid(row=i, column=0, sticky="w", padx=10, pady=(10, 5))
            ctk.CTkEntry(form_frame, textvariable=var, height=40, font=("Arial", 14)).grid(row=i, column=1, sticky="ew", padx=10, pady=(10, 5))

        # Campo de Descripción (ocupa 2 columnas)
        ctk.CTkLabel(form_frame, text="Descripción", font=("Arial", 14)).grid(row=len(fields), column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))
        self.desc_textbox = ctk.CTkTextbox(form_frame, height=150, font=("Arial", 14))
        self.desc_textbox.grid(row=len(fields) + 1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))

        # Frame de Botones
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        # Botones (Delegación de eventos al controlador a través de métodos de la vista)
        ctk.CTkButton(button_frame, text="➕ Agregar", command=self._handle_crear_articulo, height=45, 
                      fg_color="#2ecc71", hover_color="#27ae60", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", expand=True, fill="x", padx=5)
        
        self.btn_modificar = ctk.CTkButton(button_frame, text="✏️ Modificar", command=self._handle_modificar_articulo, height=45, 
                      fg_color="#f39c12", hover_color="#e67e22", font=ctk.CTkFont(size=16, weight="bold"), state="disabled")
        self.btn_modificar.pack(side="left", expand=True, fill="x", padx=5)
        
        self.btn_eliminar = ctk.CTkButton(button_frame, text="🗑️ Eliminar", command=self._handle_eliminar_articulo, height=45, 
                      fg_color="#e74c3c", hover_color="#c0392b", font=ctk.CTkFont(size=16, weight="bold"), state="disabled")
        self.btn_eliminar.pack(side="left", expand=True, fill="x", padx=5)
        
        ctk.CTkButton(button_frame, text="🧹 Limpiar", command=self.limpiar_entradas, height=45, 
                      fg_color="#95a5a6", hover_color="#7f8c8d", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", expand=True, fill="x", padx=5)

    # ----------------------------------------------------------------------
    # Métodos de Eventos (Delegación al Controlador)
    # ----------------------------------------------------------------------
    
    def _handle_crear_articulo(self):
        data = self._obtener_datos_formulario()
        self.controller.handle_crear_articulo(data["codigo"], data["articulo"], data["descripcion"])
            
    def _handle_buscar_articulo(self):
        termino = self.buscar_var.get()
        self.controller.handle_buscar_articulo(termino)
            
    def _handle_modificar_articulo(self):
        if not self.articulo_id_cargado:
            self.display_message("❌ Primero debe buscar y cargar un artículo para modificarlo.", is_success=False)
            return

        data = self._obtener_datos_formulario()
        self.controller.handle_modificar_articulo(self.articulo_id_cargado, 
                                                  data["codigo"], data["articulo"], 
                                                  data["descripcion"])
            
    def _handle_eliminar_articulo(self):
        if not self.articulo_id_cargado:
            self.display_message("❌ Primero debe buscar y cargar un artículo para eliminarlo.", is_success=False)
            return
            
        if messagebox.askyesno("⚠️ Confirmación", "¿Está seguro de que desea eliminar este artículo?"):
            self.controller.handle_eliminar_articulo(self.articulo_id_cargado)
    
    # ----------------------------------------------------------------------
    # Métodos de Mutación de Vista (Llamados por el Controlador)
    # ----------------------------------------------------------------------

    def limpiar_entradas(self): 
        """Limpia todos los campos del formulario."""
        self.buscar_var.set("")
        self.codigo_var.set("")
        self.articulo_var.set("")
        self.desc_textbox.delete("1.0", "end")
        self.articulo_id_cargado = None
        self._set_btn_state("disabled")
        self.display_message("") # Limpiar el mensaje de estado

    def _obtener_datos_formulario(self): 
        """Recolecta los datos de los campos de entrada."""
        return {
            "codigo": self.codigo_var.get(),
            "articulo": self.articulo_var.get(),
            "descripcion": self.desc_textbox.get("1.0", "end-1c").strip()
        }
        
    def _establecer_datos_formulario(self, data: dict): 
        """Establece los valores en los campos de entrada y habilita botones."""
        self.codigo_var.set(data.get("codigo", ""))
        self.articulo_var.set(data.get("articulo", ""))
        self.desc_textbox.delete("1.0", "end")
        self.desc_textbox.insert("1.0", data.get("descripcion", ""))
        self.articulo_id_cargado = data.get("id")
        self._set_btn_state("normal")
        
    def _set_btn_state(self, state):
        """Habilita o deshabilita los botones de Modificar/Eliminar."""
        self.btn_modificar.configure(state=state)
        self.btn_eliminar.configure(state=state)
        
    def display_message(self, message: str, is_success: bool = True):
        """Muestra un mensaje de estado en la interfaz."""
        color = "#2ecc71" if is_success else "#e74c3c"
        self.message_label.configure(text=message, text_color=color)