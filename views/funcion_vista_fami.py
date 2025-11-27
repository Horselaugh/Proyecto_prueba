import customtkinter as ctk
from tkinter import messagebox
from typing import Dict, List, Optional
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__))) 

from controllers.familiar_controller import FamiliarControlador 

class FamiliarViewFrame(ctk.CTkFrame):
    """
    Vista para el módulo de gestión de Familiares. 
    Hereda de CTkFrame para ser cargado en el panel de contenido de MenuApp.
    """
    
    def __init__(self, master, controller: FamiliarControlador):
        super().__init__(master, corner_radius=0, fg_color="transparent") 
        
        self.controller = controller 
        self.controller.set_view(self) # Registrar la vista en el controlador
        
        self.familiar_id_cargado: Optional[int] = None
        self.parentescos_map: Dict[str, int] = {} # Mapeo Nombre -> ID (CLAVE)
        
        # Variables de control
        self.nombre_var = ctk.StringVar(self)
        self.apellido_var = ctk.StringVar(self)
        self.parentesco_var = ctk.StringVar(self)
        self.telefono_var = ctk.StringVar(self)
        self.direccion_var = ctk.StringVar(self)
        self.tutor_var = ctk.BooleanVar(self)
        
        # Variables de búsqueda
        self.buscar_id_var = ctk.StringVar(self)
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1) # Fila 2 para la tabla (si existiera) o el contenido
        
        self._configurar_interfaz()

    # MÉTODO CLAVE: Requerido por la estructura de menu.py
    def show(self):
        """Llamado por MenuApp, invoca la carga de datos iniciales del controlador."""
        self.controller.load_initial_data() 
        # Cargar datos de la tabla si existiera una tabla (Treeview)

    def _configurar_interfaz(self):
        """Configura la interfaz gráfica (Diseño General CRUD)."""
        
        # Título y Mensaje
        self.title_label = ctk.CTkLabel(self, text="🏠 GESTIÓN DE FAMILIARES", 
                                        font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="ew")

        self.message_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14), text_color="yellow")
        self.message_label.grid(row=1, column=0, pady=5, padx=20, sticky="ew")

        # Contenedor principal para el formulario
        scroll_frame = ctk.CTkScrollableFrame(self, fg_color="#111111", corner_radius=10, label_text="DATOS PERSONALES")
        scroll_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        scroll_frame.columnconfigure((0, 1), weight=1)
        
        # Sección de Búsqueda
        search_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        search_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        search_frame.columnconfigure(0, weight=1)
        
        ctk.CTkLabel(search_frame, text="Buscar Familiar (ID)", font=("Arial", 14)).grid(row=0, column=0, sticky="w", padx=10, pady=(0, 5))
        
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.buscar_id_var, placeholder_text="ID del Familiar...", height=40)
        search_entry.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        ctk.CTkButton(search_frame, text="🔍 Buscar y Cargar", command=self._handle_buscar_familiar, height=40,
                      fg_color="#3498db", hover_color="#2980b9").grid(row=1, column=1, padx=(10, 0), pady=(0, 10))

        # Separador
        ctk.CTkFrame(scroll_frame, height=2, fg_color="#555555").grid(row=1, column=0, sticky="ew", padx=20)
        
        # Sección de Formulario (GRID dentro de main_frame)
        scroll_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        scroll_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        scroll_frame.columnconfigure((0, 1), weight=1)
        
        # Fila 0: Nombre y Apellido
        self._add_field(scroll_frame, 0, "Primer Nombre:", self.nombre_var)
        self._add_field(scroll_frame, 1, "Primer Apellido:", self.apellido_var)
        
        # Fila 2: Teléfono y Parentesco
        self._add_field(scroll_frame, 2, "Teléfono:", self.telefono_var)

        # Dropdown para Parentesco
        ctk.CTkLabel(scroll_frame, text="Parentesco:", font=("Arial", 14)).grid(row=2, column=1, sticky="w", padx=10, pady=(10, 5))
        self.parentesco_dropdown = ctk.CTkComboBox(scroll_frame, variable=self.parentesco_var, values=["Cargando..."], height=40)
        self.parentesco_dropdown.grid(row=3, column=1, sticky="ew", padx=10, pady=(0, 5))

        # Fila 4: Dirección (ocupa 2 columnas)
        ctk.CTkLabel(scroll_frame, text="Dirección:", font=("Arial", 14)).grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))
        self.direccion_entry = ctk.CTkEntry(scroll_frame, textvariable=self.direccion_var, height=40)
        self.direccion_entry.grid(row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))

        # Fila 6: Checkbox Tutor
        ctk.CTkCheckBox(scroll_frame, text="¿Es Tutor Legal?", variable=self.tutor_var, 
                        font=("Arial", 14)).grid(row=6, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 10))

        # Frame de Botones
        button_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        button_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        # Botones (Delegación de eventos al controlador a través de métodos de la vista)
        ctk.CTkButton(button_frame, text="➕ Crear Familiar", command=self._handle_crear_familiar, height=45, 
                      fg_color="#2ecc71", hover_color="#27ae60", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", expand=True, fill="x", padx=5)
        
        self.btn_modificar = ctk.CTkButton(button_frame, text="✏️ Modificar", command=self._handle_actualizar_familiar, height=45, 
                      fg_color="#f39c12", hover_color="#e67e22", font=ctk.CTkFont(size=16, weight="bold"), state="disabled")
        self.btn_modificar.pack(side="left", expand=True, fill="x", padx=5)
        
        self.btn_eliminar = ctk.CTkButton(button_frame, text="🗑️ Eliminar", command=self._handle_eliminar_familiar, height=45, 
                      fg_color="#e74c3c", hover_color="#c0392b", font=ctk.CTkFont(size=16, weight="bold"), state="disabled")
        self.btn_eliminar.pack(side="left", expand=True, fill="x", padx=5)
        
        ctk.CTkButton(button_frame, text="🧹 Limpiar", command=self.limpiar_entradas, height=45, 
                      fg_color="#95a5a6", hover_color="#7f8c8d", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", expand=True, fill="x", padx=5)

    def _add_field(self, parent, column, label_text, var):
        """Función auxiliar para añadir etiquetas y campos de entrada."""
        row = 2 * column # Fila para etiqueta
        ctk.CTkLabel(parent, text=label_text, font=("Arial", 14)).grid(row=row, column=column, sticky="w", padx=10, pady=(10, 5))
        ctk.CTkEntry(parent, textvariable=var, height=40).grid(row=row + 1, column=column, sticky="ew", padx=10, pady=(0, 5))


    # ----------------------------------------------------------------------
    # Métodos de Eventos (Delegación al Controlador)
    # ----------------------------------------------------------------------
    
    def _handle_crear_familiar(self):
        data = self._obtener_datos_formulario()
        self.controller.handle_crear_familiar(data)
            
    def _handle_buscar_familiar(self):
        termino = self.buscar_id_var.get().strip()
        if termino.isdigit():
            self.controller.handle_cargar_familiar_por_id(int(termino))
        else:
            self.display_message("❌ Ingrese un ID numérico para buscar.", is_success=False)
            self.limpiar_entradas(clean_search=False)

 
    def _handle_actualizar_familiar(self):
        if not self.familiar_id_cargado:
            self.display_message("❌ Primero debe buscar y cargar un familiar para modificarlo.", is_success=False)
            return

        data = self._obtener_datos_formulario()
        data['id'] = self.familiar_id_cargado
        self.controller.handle_actualizar_familiar(data)
            
    def _handle_eliminar_familiar(self):
        if not self.familiar_id_cargado:
            self.display_message("❌ Primero debe buscar y cargar un familiar para eliminarlo.", is_success=False)
            return
            
        if messagebox.askyesno("⚠️ Confirmación", "¿Está seguro de que desea eliminar este familiar?"):
            self.controller.handle_eliminar_familiar(self.familiar_id_cargado)
    
    # ----------------------------------------------------------------------
    # Métodos de Mutación de Vista (Llamados por el Controlador)
    # ----------------------------------------------------------------------

    def limpiar_entradas(self, clean_search=True): 
        """Limpia todos los campos del formulario."""
        if clean_search: self.buscar_id_var.set("")
        self.nombre_var.set("")
        self.apellido_var.set("")
        
        # --- MODIFICACIÓN CLAVE (Limpieza) ---
        # Mantener el primer parentesco cargado si existe, sino limpiar.
        if self.parentescos_map:
            self.parentesco_var.set(list(self.parentescos_map.keys())[0])
        else:
             self.parentesco_var.set("")
             
        self.telefono_var.set("")
        self.direccion_var.set("")
        self.tutor_var.set(False)
        self.familiar_id_cargado = None
        self._set_btn_state("disabled")
        self.display_message("") # Limpiar el mensaje de estado

    def _obtener_datos_formulario(self): 
        """Recolecta los datos de los campos de entrada."""
        parentesco_nombre = self.parentesco_var.get()
        # --- MODIFICACIÓN CLAVE (Obtener ID) ---
        # Si el parentesco_nombre no existe en el mapa (ej: vacío), parentesco_id será None
        parentesco_id = self.parentescos_map.get(parentesco_nombre)
        
        return {
            "primer_nombre": self.nombre_var.get().strip(),
            "primer_apellido": self.apellido_var.get().strip(),
            "parentesco_id": parentesco_id, # Se pasa el ID, no el nombre
            "direccion": self.direccion_var.get().strip(),
            "telefono": self.telefono_var.get().strip(),
            "tutor": self.tutor_var.get()
            # Los campos segundo_nombre y segundo_apellido se ignoran por simplicidad, se manejarían si existieran en la interfaz
        }
        
    def _establecer_datos_formulario(self, data: dict): 
        """Establece los valores en los campos de entrada y habilita botones."""
        self.nombre_var.set(data.get("primer_nombre", ""))
        self.apellido_var.set(data.get("primer_apellido", ""))
        self.parentesco_var.set(data.get("parentesco_desc", "")) # Usa la descripción del parentesco
        self.telefono_var.set(data.get("telefono", ""))
        self.direccion_var.set(data.get("direccion", ""))
        # Convertir el valor de la base de datos (0/1) a booleano
        tutor_value = data.get("tutor", 0)
        self.tutor_var.set(bool(int(tutor_value)) if isinstance(tutor_value, (int, float)) else bool(tutor_value))

        self.familiar_id_cargado = data.get("id")
        self.buscar_id_var.set(str(data.get("id", ""))) # Carga el ID en el campo de búsqueda
        self._set_btn_state("normal")
        
    def _cargar_parentescos(self, parentescos: List[Dict]):
        """Carga las opciones en el ComboBox de parentescos."""
        nombres = [p['nombre'] for p in parentescos]
        self.parentescos_map = {p['nombre']: p['id'] for p in parentescos}
        self.parentesco_dropdown.configure(values=nombres)
        if nombres:
             self.parentesco_var.set(nombres[0])
        
    def _set_btn_state(self, state):
        """Habilita o deshabilita los botones de Modificar/Eliminar."""
        self.btn_modificar.configure(state=state)
        self.btn_eliminar.configure(state=state)
        
    def display_message(self, message: str, is_success: bool = True):
        """Muestra un mensaje de estado en la interfaz."""
        color = "#2ecc71" if is_success else "#e74c3c"
        self.message_label.configure(text=message, text_color=color)