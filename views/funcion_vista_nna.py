import customtkinter as ctk
from tkinter import messagebox
from typing import Dict, List, Optional
import datetime
from controllers.nna_controller import NNAControlador

# ----------------------------------------------------------------------
# CLASE DE VISTA ADAPTADA
# ----------------------------------------------------------------------

class NNAViewFrame(ctk.CTkFrame):
    """
    Vista para el módulo de gestión de NNA (Niños, Niñas y Adolescentes). 
    Hereda de CTkFrame.
    """
    
    def __init__(self, master, controller: NNAControlador):
        super().__init__(master, corner_radius=0, fg_color="transparent") 
        
        self.controller = controller 
        self.controller.set_view(self) # Registrar la vista
        
        self.nna_id_cargado: Optional[int] = None
        
        # Variables de control
        self.buscar_id_var = ctk.StringVar(self)
        self.doc_id_var = ctk.StringVar(self)
        self.p_nombre_var = ctk.StringVar(self)
        self.s_nombre_var = ctk.StringVar(self)
        self.p_apellido_var = ctk.StringVar(self)
        self.s_apellido_var = ctk.StringVar(self)
        self.f_nacimiento_var = ctk.StringVar(self, value=datetime.date.today().isoformat())
        self.genero_var = ctk.StringVar(self)
        self.telefono_var = ctk.StringVar(self)
        self.direccion_var = ctk.StringVar(self)
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1) 
        
        self._configurar_interfaz()

    # MÉTODO CLAVE: Requerido por la estructura de menu.py
    def show(self):
        """Llamado por MenuApp, invoca la carga de datos iniciales del controlador."""
        self.controller.load_initial_data() 

    def _configurar_interfaz(self):
        """Configura la interfaz gráfica (Diseño General CRUD)."""
        
        # Título y Mensaje
        self.title_label = ctk.CTkLabel(self, text="👶 GESTIÓN DE NNA", 
                                        font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="ew")

        self.message_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14), text_color="yellow")
        self.message_label.grid(row=1, column=0, pady=5, padx=20, sticky="ew")

        # Contenedor principal scrollable para el formulario largo
        scroll_frame = ctk.CTkScrollableFrame(self, fg_color="#3c3c3c", corner_radius=10, label_text="DATOS PERSONALES")
        scroll_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        scroll_frame.columnconfigure((0, 1), weight=1)
        
        # --- Sección de Búsqueda ---
        search_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        search_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="ew")
        search_frame.columnconfigure(0, weight=1)
        
        ctk.CTkLabel(search_frame, text="Buscar NNA (ID)", font=("Arial", 14)).grid(row=0, column=0, sticky="w", padx=10, pady=(5, 5))
        
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.buscar_id_var, placeholder_text="ID del NNA...", height=40)
        search_entry.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        ctk.CTkButton(search_frame, text="🔍 Buscar y Cargar", command=self._handle_buscar_nna, height=40,
                      fg_color="#3498db", hover_color="#2980b9").grid(row=1, column=1, padx=(10, 0), pady=(0, 10))

        # --- Campos del Formulario ---
        # Fila 1: Nombres
        self._add_field(scroll_frame, 2, 0, "Primer Nombre (Obligatorio):", self.p_nombre_var)
        self._add_field(scroll_frame, 2, 1, "Segundo Nombre:", self.s_nombre_var)
        
        # Fila 2: Apellidos
        self._add_field(scroll_frame, 4, 0, "Primer Apellido (Obligatorio):", self.p_apellido_var)
        self._add_field(scroll_frame, 4, 1, "Segundo Apellido:", self.s_apellido_var)
        
        # Fila 3: Cédula/Identificación y Fecha de Nacimiento
        self._add_field(scroll_frame, 6, 0, "Documento de Identidad (Opcional):", self.doc_id_var)
        self._add_field(scroll_frame, 6, 1, "Fecha de Nacimiento (YYYY-MM-DD):", self.f_nacimiento_var)
        
        # Fila 4: Género y Teléfono
        self._add_field(scroll_frame, 8, 0, "Género:", self.genero_var, is_combo=True)
        self._add_field(scroll_frame, 8, 1, "Teléfono (11 dígitos):", self.telefono_var)

        # Fila 5: Dirección
        self._add_field(scroll_frame, 10, 0, "Dirección:", self.direccion_var, columnspan=2)
        
        # Frame de Botones
        button_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        button_frame.grid(row=12, column=0, columnspan=2, padx=10, pady=(20, 10), sticky="ew")
        
        # Botones
        ctk.CTkButton(button_frame, text="➕ Crear NNA", command=self._handle_crear_nna, height=45, 
                      fg_color="#2ecc71", hover_color="#27ae60", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", expand=True, fill="x", padx=5)
        
        self.btn_modificar = ctk.CTkButton(button_frame, text="✏️ Modificar", command=self._handle_actualizar_nna, height=45, 
                      fg_color="#f39c12", hover_color="#e67e22", font=ctk.CTkFont(size=16, weight="bold"), state="disabled")
        self.btn_modificar.pack(side="left", expand=True, fill="x", padx=5)
        
        self.btn_eliminar = ctk.CTkButton(button_frame, text="🗑️ Eliminar", command=self._handle_eliminar_nna, height=45, 
                      fg_color="#e74c3c", hover_color="#c0392b", font=ctk.CTkFont(size=16, weight="bold"), state="disabled")
        self.btn_eliminar.pack(side="left", expand=True, fill="x", padx=5)
        
        ctk.CTkButton(button_frame, text="🧹 Limpiar", command=self.limpiar_entradas, height=45, 
                      fg_color="#95a5a6", hover_color="#7f8c8d", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", expand=True, fill="x", padx=5)

    def _add_field(self, parent, row, column, label_text, var, is_combo=False, columnspan=1):
        """Función auxiliar para añadir etiquetas y campos de entrada/combobox."""
        ctk.CTkLabel(parent, text=label_text, font=("Arial", 14)).grid(row=row, column=column, columnspan=columnspan, sticky="w", padx=10, pady=(10, 5))
        
        if is_combo:
            self.genero_combo = ctk.CTkComboBox(parent, variable=var, values=["Cargando..."], height=40)
            self.genero_combo.grid(row=row + 1, column=column, columnspan=columnspan, sticky="ew", padx=10, pady=(0, 5))
        else:
            ctk.CTkEntry(parent, textvariable=var, height=40).grid(row=row + 1, column=column, columnspan=columnspan, sticky="ew", padx=10, pady=(0, 5))

    
    def _handle_crear_nna(self):
        data = self._obtener_datos_formulario()
        self.controller.handle_crear_nna(data)
            
    def _handle_buscar_nna(self):
        termino = self.buscar_id_var.get().strip()
        if termino.isdigit():
            self.controller.handle_cargar_nna_por_id(int(termino))
        else:
            self.display_message("❌ Ingrese un ID numérico para buscar.", is_success=False)
            self.limpiar_entradas(clean_search=False)

            
    def _handle_actualizar_nna(self):
        if not self.nna_id_cargado:
            self.display_message("❌ Primero debe buscar y cargar un NNA para modificarlo.", is_success=False)
            return

        data = self._obtener_datos_formulario()
        data['id'] = self.nna_id_cargado
        self.controller.handle_actualizar_nna(data)
            
    def _handle_eliminar_nna(self):
        if not self.nna_id_cargado:
            self.display_message("❌ Primero debe buscar y cargar un NNA para eliminarlo.", is_success=False)
            return
            
        nombre = f"{self.p_nombre_var.get()} {self.p_apellido_var.get()}"
        if messagebox.askyesno("⚠️ Confirmación", f"¿Está seguro de que desea eliminar a {nombre} (ID: {self.nna_id_cargado})?"):
            self.controller.handle_eliminar_nna(self.nna_id_cargado)
    
    # ----------------------------------------------------------------------
    # Métodos de Mutación de Vista (Llamados por el Controlador)
    # ----------------------------------------------------------------------

    def limpiar_entradas(self, clean_search=True): 
        """Limpia todos los campos del formulario."""
        if clean_search: self.buscar_id_var.set("")
        self.doc_id_var.set("")
        self.p_nombre_var.set("")
        self.s_nombre_var.set("")
        self.p_apellido_var.set("")
        self.s_apellido_var.set("")
        self.f_nacimiento_var.set(datetime.date.today().isoformat())
        
        # Mantener el primer género seleccionado o limpiar
        if hasattr(self, 'genero_combo') and self.genero_combo.cget("values"):
             self.genero_var.set(self.genero_combo.cget("values")[0])
        else:
             self.genero_var.set("")
             
        self.telefono_var.set("")
        self.direccion_var.set("")
        self.nna_id_cargado = None
        self._set_btn_state("disabled")
        self.display_message("")

    def _obtener_datos_formulario(self): 
        """Recolecta los datos de los campos de entrada."""
        doc_id = self.doc_id_var.get().strip()
        
        return {
            "primer_nombre": self.p_nombre_var.get().strip(),
            "segundo_nombre": self.s_nombre_var.get().strip() or None,
            "primer_apellido": self.p_apellido_var.get().strip(),
            "segundo_apellido": self.s_apellido_var.get().strip() or None,
            # CORRECCIÓN: Se pasa None si el campo está vacío
            "documento_identidad": doc_id if doc_id else None, 
            "fecha_nacimiento": self.f_nacimiento_var.get().strip(),
            "genero": self.genero_var.get(),
            "direccion": self.direccion_var.get().strip(),
            "telefono": self.telefono_var.get().strip()
        }
        
    def _establecer_datos_formulario(self, data: dict): 
        """Establece los valores en los campos de entrada y habilita botones."""
        self.p_nombre_var.set(data.get("primer_nombre", ""))
        self.s_nombre_var.set(data.get("segundo_nombre", "") or "")
        self.p_apellido_var.set(data.get("primer_apellido", ""))
        self.s_apellido_var.set(data.get("segundo_apellido", "") or "")
        self.doc_id_var.set(data.get("documento_identidad", "") or "")
        self.f_nacimiento_var.set(data.get("fecha_nacimiento", datetime.date.today().isoformat()))
        self.genero_var.set(data.get("genero", ""))
        self.telefono_var.set(data.get("telefono", ""))
        self.direccion_var.set(data.get("direccion", ""))
        
        self.nna_id_cargado = data.get("id")
        self.buscar_id_var.set(str(data.get("id", "")))
        self._set_btn_state("normal")
        
    def _cargar_generos(self, generos: List[str]):
        """Carga las opciones en el ComboBox de Género."""
        if generos:
            self.genero_combo.configure(values=generos)
            # Asegurar que se selecciona el primero por defecto si la variable está vacía
            if not self.genero_var.get():
                self.genero_var.set(generos[0])
        
    def _set_btn_state(self, state):
        """Habilita o deshabilita los botones de Modificar/Eliminar."""
        self.btn_modificar.configure(state=state)
        self.btn_eliminar.configure(state=state)
        
    def display_message(self, message: str, is_success: bool = True):
        """Muestra un mensaje de estado en la interfaz."""
        color = "#2ecc71" if is_success else "#e74c3c"
        self.message_label.configure(text=message, text_color=color)