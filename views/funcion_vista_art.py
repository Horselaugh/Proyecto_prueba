import customtkinter as ctk
from tkinter import messagebox
import sys
import os

# ----------------------------------------------------------------------
# Configuración de Paths e Importaciones
# ----------------------------------------------------------------------
# Asegura que el path del proyecto sea accesible para importar el modelo y el controlador
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    if project_root not in sys.path:
        sys.path.append(project_root)
except NameError:
    pass

class ArticuloVista(ctk.CTkFrame):
    
    # MODIFICACIÓN CLAVE: Recibir el master (el frame contenedor en MenuApp) y el controller
    def __init__(self, master, controller=None):
        super().__init__(master, fg_color="transparent") # Inicializa como un frame dentro de master
        
        
        self.articulo_id_cargado = None
        
        # Variables de control
        self.buscar_var = ctk.StringVar(self)
        self.codigo_var = ctk.StringVar(self)
        self.articulo_var = ctk.StringVar(self)
        self.descripcion_var = ctk.StringVar(self)
        
        self.crear_interfaz()
        
        # Se llama a los métodos de obtención inicial solo si el controlador real lo permite.
        # En este contexto, ArticuloVista no maneja una lista visible, por lo que no es necesario.
        
    def crear_interfaz(self):
        # Frame principal - Ya es ArticuloVista (self) que hereda de ctk.CTkFrame
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Título y Mensajes
        self.title_label = ctk.CTkLabel(self, text="📦 GESTIÓN DE ARTÍCULOS LOPNNA", 
                                        font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="ew")

        self.message_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14), text_color="yellow")
        self.message_label.grid(row=1, column=0, pady=5, padx=20, sticky="ew")

        # Contenedor principal de formulario y búsqueda
        content_frame = ctk.CTkFrame(self, fg_color="#3c3c3c", corner_radius=10)
        content_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        content_frame.columnconfigure(0, weight=1)

        # Frame de Búsqueda
        search_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        search_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        search_frame.columnconfigure(0, weight=1)
        
        ctk.CTkLabel(search_frame, text="Buscar Artículo (Código)", font=("Arial", 14)).grid(row=0, column=0, sticky="w", padx=10, pady=(0, 5))
        
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.buscar_var, placeholder_text="Ingrese Código...", height=40)
        search_entry.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        ctk.CTkButton(search_frame, text="🔍 Buscar", command=self.buscar_articulo, height=40,
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
        
        # Botones
        ctk.CTkButton(button_frame, text="➕ Agregar", command=self.crear_articulo, height=45, 
                      fg_color="#2ecc71", hover_color="#27ae60", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", expand=True, fill="x", padx=5)
        ctk.CTkButton(button_frame, text="✏️ Modificar", command=self.modificar_articulo, height=45, 
                      fg_color="#f39c12", hover_color="#e67e22", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", expand=True, fill="x", padx=5)
        ctk.CTkButton(button_frame, text="🗑️ Eliminar", command=self.eliminar_articulo, height=45, 
                      fg_color="#e74c3c", hover_color="#c0392b", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", expand=True, fill="x", padx=5)
        ctk.CTkButton(button_frame, text="🧹 Limpiar", command=self.limpiar_entradas, height=45, 
                      fg_color="#95a5a6", hover_color="#7f8c8d", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", expand=True, fill="x", padx=5)

    # ----------------------------------------------------------------------
    # Métodos de Eventos (Controlador)
    # ----------------------------------------------------------------------
    
    def crear_articulo(self):
        data = self._obtener_datos_formulario()
        resultado = self.controller.crear_articulo(data["codigo"], data["articulo"], data["descripcion"])
        self.display_message(resultado["message"], is_success=(resultado["status"] == "success"))
        if resultado["status"] == "success":
            self.limpiar_entradas()
            
    def buscar_articulo(self):
        termino = self.buscar_var.get()
        if not termino:
            self.display_message("❌ Ingrese un código para buscar.", is_success=False)
            return
            
        resultado = self.controller.buscar_articulo(termino)
        self.display_message(resultado["message"], is_success=(resultado["status"] == "success"))
        
        if resultado["status"] == "success":
            data = resultado["data"]
            self._establecer_datos_formulario(data)
            self.articulo_id_cargado = data["id"]
        else:
            self.limpiar_entradas()
            self.articulo_id_cargado = None
            
    def modificar_articulo(self):
        if not self.articulo_id_cargado:
            self.display_message("❌ Primero debe buscar y cargar un artículo para modificarlo.", is_success=False)
            return

        data = self._obtener_datos_formulario()
        resultado = self.controller.modificar_articulo(self.articulo_id_cargado, 
                                                       data["codigo"], data["articulo"], 
                                                       data["descripcion"])
        
        self.display_message(resultado["message"], is_success=(resultado["status"] == "success"))
        if resultado["status"] == "success":
            self.limpiar_entradas()
            self.articulo_id_cargado = None
            
    def eliminar_articulo(self):
        if not self.articulo_id_cargado:
            self.display_message("❌ Primero debe buscar y cargar un artículo para eliminarlo.", is_success=False)
            return
            
        # Nota: Idealmente se usaría un modal de confirmación aquí, no messagebox
        if messagebox.askyesno("⚠️ Confirmación", "¿Está seguro de que desea eliminar este artículo?"):
            resultado = self.controller.eliminar_articulo(self.articulo_id_cargado)
            
            self.display_message(resultado["message"], is_success=(resultado["status"] == "success"))
            if resultado["status"] == "success":
                self.limpiar_entradas()
                self.articulo_id_cargado = None
    
    # --- Métodos de Ayuda ---

    def _obtener_datos_formulario(self): 
        """Recolecta los datos de los campos de entrada."""
        return {
            "codigo": self.codigo_var.get(),
            "articulo": self.articulo_var.get(),
            "descripcion": self.desc_textbox.get("1.0", "end-1c").strip()
        }
        
    def _establecer_datos_formulario(self, data: dict): 
        """Establece los valores en los campos de entrada."""
        self.codigo_var.set(data.get("codigo", ""))
        self.articulo_var.set(data.get("articulo", ""))
        self.desc_textbox.delete("1.0", "end")
        self.desc_textbox.insert("1.0", data.get("descripcion", ""))
        
    def limpiar_entradas(self): 
        """Limpia todos los campos del formulario."""
        self.buscar_var.set("")
        self.codigo_var.set("")
        self.articulo_var.set("")
        self.desc_textbox.delete("1.0", "end")
        self.articulo_id_cargado = None
        self.display_message("") # Limpiar el mensaje de estado
        
    def display_message(self, message: str, is_success: bool = True):
        """Muestra un mensaje de estado en la interfaz."""
        color = "#2ecc71" if is_success else "#e74c3c"
        self.message_label.configure(text=message, text_color=color)

# ----------------------------------------------------------------------
# ELIMINACIÓN DEL BLOQUE MAIN
# ----------------------------------------------------------------------
# Se elimina el bloque if __name__ == "__main__": main()
# para que el módulo solo exporte la clase ArticuloVista.