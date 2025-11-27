import customtkinter as ctk
from tkinter import ttk, messagebox
from typing import List, Dict, Any, Optional
import sys
import os

# ----------------------------------------------------------------------
# 1. Importación del Controlador Real
# ----------------------------------------------------------------------

# Añadir el directorio superior y el actual al path para las importaciones
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    # Importar el controlador real, asumiendo que está en el mismo path.
    from controllers.unidad_educativa_controller import UnidadEducativaControlador
except ImportError:
    # Si la importación falla, detener la ejecución.
    print("Error: No se pudo importar UnidadEducativaControlador. Asegúrese de que 'unidad_educativa_controller.py' esté disponible.")
    sys.exit(1)

# Asignar la clase importada al nombre usado para la anotación
ControladorDeUnidadEducativa = UnidadEducativaControlador


# ----------------------------------------------------------------------
# 2. La Vista CTkFrame
# ----------------------------------------------------------------------

class UnidadEducativaViewFrame(ctk.CTkFrame):
    """
    Vista para el módulo de Unidades Educativas. Hereda de CTkFrame.
    Implementa la interfaz de CRUD y delega acciones al controlador.
    """
    
    # Usamos el nombre de la clase real en la anotación
    def __init__(self, master, controller: ControladorDeUnidadEducativa):
        super().__init__(master, corner_radius=0, fg_color="transparent") 
        
        self.controller = controller 
        self.controller.set_view(self) 
        
        self.ue_id_cargada: Optional[int] = None # ID de la UE si está en modo edición
        
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(2, weight=1) 
        
        # Variables de control
        self.nombre_var = ctk.StringVar(self)
        self.director_var = ctk.StringVar(self)
        self.tipo_var = ctk.StringVar(self, value="Pública")
        self.telefono_var = ctk.StringVar(self)
        self.direccion_var = ctk.StringVar(self)
        self.buscar_id_var = ctk.StringVar(self)
        self.buscar_nombre_var = ctk.StringVar(self)

        self._configurar_interfaz()

    def show(self):
        """Llamado por MenuApp, invoca la carga de datos iniciales del controlador."""
        self.controller.load_initial_data() 

    def _configurar_interfaz(self):
        """Crea y posiciona todos los widgets de la interfaz."""
        
        # Fila 0: Título y Mensaje
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=0, column=0, columnspan=2, pady=(20, 10), padx=20, sticky="ew")
        title_frame.columnconfigure(0, weight=1)
        
        self.title_label = ctk.CTkLabel(title_frame, text="🏫 GESTIÓN DE UNIDADES EDUCATIVAS", 
                                        font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, sticky="ew")

        # Mensaje de estado, inicialmente vacío
        self.message_label = ctk.CTkLabel(title_frame, text="", font=ctk.CTkFont(size=14), text_color="#2ecc71")
        self.message_label.grid(row=1, column=0, pady=5, sticky="ew")

        # Fila 1: Frame de Formulario
        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=(10, 20))
        form_frame.columnconfigure((0, 1), weight=1)
        
        ctk.CTkLabel(form_frame, text="Nombre:", anchor="w").grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        ctk.CTkEntry(form_frame, textvariable=self.nombre_var).grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        
        ctk.CTkLabel(form_frame, text="Director:", anchor="w").grid(row=0, column=1, padx=10, pady=(10, 5), sticky="w")
        ctk.CTkEntry(form_frame, textvariable=self.director_var).grid(row=1, column=1, padx=10, pady=(0, 10), sticky="ew")

        ctk.CTkLabel(form_frame, text="Tipo:", anchor="w").grid(row=2, column=0, padx=10, pady=(10, 5), sticky="w")
        ctk.CTkComboBox(form_frame, variable=self.tipo_var, values=["Pública", "Privada"]).grid(row=3, column=0, padx=10, pady=(0, 10), sticky="ew")

        ctk.CTkLabel(form_frame, text="Teléfono:", anchor="w").grid(row=2, column=1, padx=10, pady=(10, 5), sticky="w")
        ctk.CTkEntry(form_frame, textvariable=self.telefono_var).grid(row=3, column=1, padx=10, pady=(0, 10), sticky="ew")

        ctk.CTkLabel(form_frame, text="Dirección:", anchor="w").grid(row=4, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")
        ctk.CTkEntry(form_frame, textvariable=self.direccion_var).grid(row=5, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

        # Botones de Acción
        self.btn_crear = ctk.CTkButton(form_frame, text="➕ Registrar", command=self._handle_crear_actualizar, 
                                        fg_color="#2ecc71", hover_color="#27ae60")
        self.btn_crear.grid(row=6, column=0, padx=10, pady=(10, 20), sticky="ew")
        
        self.btn_limpiar = ctk.CTkButton(form_frame, text="🧹 Limpiar", command=self.limpiar_formulario,
                                          fg_color="#f39c12", hover_color="#e67e22")
        self.btn_limpiar.grid(row=6, column=1, padx=10, pady=(10, 20), sticky="ew")
        
        # El botón de eliminar se deshabilita hasta que se carga una UE para edición
        self.btn_eliminar = ctk.CTkButton(form_frame, text="🗑️ Eliminar", command=self._handle_eliminar, 
                                         fg_color="#e74c3c", hover_color="#c0392b", state="disabled")
        self.btn_eliminar.grid(row=7, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")


        # Fila 1: Frame de Búsqueda y Lista (Derecha)
        list_frame = ctk.CTkFrame(self)
        list_frame.grid(row=1, column=1, rowspan=2, sticky="nsew", padx=(10, 20), pady=(10, 20))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(4, weight=1) # El Treeview crece
        
        # Búsqueda por ID
        ctk.CTkLabel(list_frame, text="Buscar por ID:", anchor="w").grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        search_id_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        search_id_frame.grid(row=1, column=0, sticky="ew", padx=10)
        search_id_frame.columnconfigure(0, weight=1)
        ctk.CTkEntry(search_id_frame, textvariable=self.buscar_id_var, placeholder_text="ID de la UE").grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ctk.CTkButton(search_id_frame, text="🔍 ID", command=self._handle_buscar_id, width=50).grid(row=0, column=1)

        # Búsqueda por Nombre (y botón Listar)
        ctk.CTkLabel(list_frame, text="Buscar por Nombre/Listar Todos:", anchor="w").grid(row=2, column=0, padx=10, pady=(10, 5), sticky="w")
        search_name_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        search_name_frame.grid(row=3, column=0, sticky="ew", padx=10)
        search_name_frame.columnconfigure(0, weight=1)
        ctk.CTkEntry(search_name_frame, textvariable=self.buscar_nombre_var, placeholder_text="Nombre de la UE").grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ctk.CTkButton(search_name_frame, text="🔍 Nom.", command=self._handle_buscar_nombre, width=70).grid(row=0, column=1, padx=(0, 5))
        ctk.CTkButton(search_name_frame, text="🔄 Todos", command=self.controller.load_initial_data, width=70).grid(row=0, column=2)

        # Treeview (Tabla de Resultados)
        self.treeview_frame = ctk.CTkFrame(list_frame)
        self.treeview_frame.grid(row=4, column=0, sticky="nsew", padx=10, pady=(10, 10))
        self.treeview_frame.columnconfigure(0, weight=1)
        self.treeview_frame.rowconfigure(0, weight=1)
        
        # Configurar Treeview con estilo TTK para temas oscuros
        style = ttk.Style()
        style.theme_use("default") 
        style.configure("Treeview", 
                        background="#2b2b2b", 
                        foreground="white", 
                        rowheight=25, 
                        fieldbackground="#2b2b2b", 
                        font=('Arial', 10))
        style.map('Treeview', 
                  background=[('selected', '#3498db')])
                  
        self.treeview = ttk.Treeview(self.treeview_frame, columns=("ID", "Nombre", "Director", "Tipo", "Teléfono"), show='headings')
        self.treeview.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar vertical (CustomTkinter)
        self.scrollbar = ctk.CTkScrollbar(self.treeview_frame, command=self.treeview.yview)
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        self.treeview.configure(yscrollcommand=self.scrollbar.set)
        
        # Definir encabezados y columnas
        self.treeview.heading("ID", text="ID")
        self.treeview.column("ID", width=40, anchor="center")
        self.treeview.heading("Nombre", text="Nombre")
        self.treeview.column("Nombre", width=180)
        self.treeview.heading("Director", text="Director")
        self.treeview.column("Director", width=120)
        self.treeview.heading("Tipo", text="Tipo")
        self.treeview.column("Tipo", width=80)
        self.treeview.heading("Teléfono", text="Teléfono")
        self.treeview.column("Teléfono", width=100)

        # Vincular evento de selección
        self.treeview.bind('<<TreeviewSelect>>', self._on_treeview_select)
        
        
    # ----------------------------------------------------------------------
    # Métodos de Eventos (Delegación al Controlador)
    # ----------------------------------------------------------------------

    def _handle_crear_actualizar(self):
        """Maneja la acción de Crear o Actualizar."""
        data = self._obtener_datos_formulario()
        
        if not data['nombre'] or not data['director'] or not data['telefono']:
            self.display_message("❌ Nombre, director y teléfono son obligatorios.", False)
            return

        if self.ue_id_cargada:
            # Modo edición/actualización
            self.controller.handle_actualizar_ue(self.ue_id_cargada, data)
        else:
            # Modo creación
            self.controller.handle_crear_ue(data)
            
    def _handle_buscar_id(self):
        """Maneja la búsqueda por ID."""
        id_str = self.buscar_id_var.get().strip()
        if not id_str:
            self.display_message("❌ Ingrese un ID para buscar.", False)
            self.controller.load_initial_data()
            return

        try:
            id_ue = int(id_str)
            self.controller.handle_buscar_ue(busqueda_id=id_ue)
        except ValueError:
            self.display_message("❌ Ingrese un ID numérico válido para buscar.", False)
            self.controller.load_initial_data()

    def _handle_buscar_nombre(self):
        """Maneja la búsqueda por Nombre."""
        nombre_str = self.buscar_nombre_var.get().strip()
        if not nombre_str:
            self.controller.load_initial_data() # Listar todos si la búsqueda está vacía
            return
            
        self.controller.handle_buscar_ue(busqueda_nombre=nombre_str)

    def _handle_eliminar(self):
        """Maneja la eliminación (requiere confirmación)."""
        if not self.ue_id_cargada:
            self.display_message("❌ Primero debe cargar una Unidad Educativa para eliminar.", False)
            return
            
        if messagebox.askyesno("Confirmar Eliminación", 
                               f"¿Está seguro de eliminar la Unidad Educativa ID {self.ue_id_cargada}? Esta acción es irreversible (eliminación física)."):
            self.controller.handle_eliminar_ue(self.ue_id_cargada)

    def _on_treeview_select(self, event):
        """Carga los datos del elemento seleccionado en el Treeview al formulario."""
        # Limpiar la selección previa para evitar disparar el evento múltiples veces
        if not self.treeview.selection():
            return
            
        selected_item = self.treeview.focus()
        if not selected_item:
            return
            
        # Obtener los valores de la fila seleccionada (ID es el primer valor)
        values = self.treeview.item(selected_item, 'values')
        if values:
            try:
                # El ID es el primer valor
                id_ue = int(values[0])
                # Delegar la carga completa al controlador
                self.controller.handle_cargar_ue_para_edicion(id_ue)
            except ValueError:
                self.display_message("Error: ID no válido en la selección.", False)

    # ----------------------------------------------------------------------
    # Métodos de Mutación de Vista (Llamados por el Controlador)
    # ----------------------------------------------------------------------

    def _obtener_datos_formulario(self) -> Dict[str, Any]:
        """Recopila los datos del formulario."""
        return {
            "nombre": self.nombre_var.get().strip(),
            "director": self.director_var.get().strip(),
            "tipo": self.tipo_var.get(), # Tipo viene como 'Pública' o 'Privada'
            "telefono": self.telefono_var.get().strip(),
            "direccion": self.direccion_var.get().strip()
        }
        
    def _establecer_datos_formulario(self, data: Dict[str, Any], id_ue: Optional[int]):
        """Establece los valores en los campos de entrada y configura el modo edición."""
        self.ue_id_cargada = id_ue
        self.nombre_var.set(data.get("nombre", ""))
        self.director_var.set(data.get("director", ""))
        # El controlador ya capitalizó el tipo (e.g., de 'PUBLICA' a 'Pública')
        self.tipo_var.set(data.get("tipo", "Pública")) 
        self.telefono_var.set(data.get("telefono", ""))
        self.direccion_var.set(data.get("direccion", ""))
        
        # Cambiar el texto del botón y habilitar eliminar
        self.btn_crear.configure(text="💾 Guardar Cambios", fg_color="#3498db", hover_color="#2980b9")
        self.btn_eliminar.configure(state="normal")
        
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario y vuelve al modo creación."""
        self.ue_id_cargada = None
        self.nombre_var.set("")
        self.director_var.set("")
        self.tipo_var.set("Pública")
        self.telefono_var.set("")
        self.direccion_var.set("")
        self.buscar_id_var.set("")
        self.buscar_nombre_var.set("")
        
        # Restaurar el texto del botón y deshabilitar eliminar
        self.btn_crear.configure(text="➕ Registrar", fg_color="#2ecc71", hover_color="#27ae60")
        self.btn_eliminar.configure(state="disabled")
        self.display_message("") # Limpiar mensaje

    def display_list(self, data: List[Dict[str, Any]]):
        """Muestra la lista de Unidades Educativas en el Treeview."""
        # Limpiar tabla
        for item in self.treeview.get_children():
            self.treeview.delete(item)
            
        if not data:
            return

        for item in data:
            # Insertar los campos relevantes en el orden de las columnas
            values = (
                item.get('id', 'N/A'),
                item.get('nombre', ''),
                item.get('director', ''),
                # Capitalizar el tipo para la visualización (e.g., 'PUBLICA' -> 'Pública')
                item.get('tipo', '').capitalize(), 
                item.get('telefono', '')
            )
            self.treeview.insert('', 'end', values=values)

    def display_message(self, message: str, is_success: bool = True):
        """Muestra un mensaje de estado en la interfaz."""
        color = "#2ecc71" if is_success else "#e74c3c"
        self.message_label.configure(text=message, text_color=color)