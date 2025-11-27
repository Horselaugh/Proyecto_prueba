import customtkinter as ctk
from tkinter import messagebox, N, S, E, W
from typing import Dict, List, Optional
import datetime

# Se importa la clase real del controlador para la vista.
# Se asume que matricula_controller.py está en la carpeta 'controllers'
from controllers.matricula_controller import MatriculaControlador 

# ----------------------------------------------------------------------
# CLASE DE VISTA ADAPTADA
# ----------------------------------------------------------------------

class MatriculaViewFrame(ctk.CTkFrame):
    """
    Vista para el módulo de gestión de Matrículas. 
    Hereda de CTkFrame para ser cargado en el panel de contenido de MenuApp.
    """
    
    # Se define la dependencia del controlador real
    def __init__(self, master, controller: MatriculaControlador):
        super().__init__(master, corner_radius=0, fg_color="transparent") 
        
        self.controller = controller 
        self.controller.set_view(self) # Enlaza la vista al controlador
        
        # Mapeos
        self.nna_map: Dict[str, int] = {} # Nombre NNA -> ID
        self.unidad_map: Dict[str, int] = {} # Nombre Unidad -> ID
        
        # Variables de control
        self.nna_var = ctk.StringVar(self, value="Seleccionar NNA")
        self.unidad_var = ctk.StringVar(self, value="Seleccionar Unidad")
        self.grado_var = ctk.StringVar(self, value="Seleccionar Grado")
        self.fecha_matricula_var = ctk.StringVar(self, value=datetime.date.today().isoformat())
        self.activa_var = ctk.BooleanVar(self, value=True)
        
        self.matricula_cargada_id: Optional[Dict[str, int]] = None # {'nna_id': x, 'unidad_id': y}
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        
        self._configurar_interfaz()

    # MÉTODO CLAVE: Inicia la carga de datos
    def show(self):
        """Llamado por la aplicación principal, invoca la carga de datos iniciales del controlador."""
        self.controller.load_initial_data() 

    def _configurar_interfaz(self):
        """Configura la interfaz gráfica (Diseño General CRUD)."""
        
        # Título y Mensaje
        self.title_label = ctk.CTkLabel(self, text="🎓 GESTIÓN DE MATRÍCULAS", 
                                        font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="ew")

        self.message_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14), text_color="yellow")
        self.message_label.grid(row=1, column=0, pady=5, padx=20, sticky="ew")

        # Contenedor principal para el formulario
        main_frame = ctk.CTkFrame(self, fg_color="#111111", corner_radius=10)
        main_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        main_frame.columnconfigure((0, 1), weight=1)
        
        # Dropdowns de selección
        self._create_selection_widgets(main_frame, 0, "NNA:", self.nna_var)
        self._create_selection_widgets(main_frame, 1, "Unidad Educativa:", self.unidad_var)
        
        # Separador
        ctk.CTkFrame(main_frame, height=2, fg_color="#555555").grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=(10, 10))
        
        # Campos de Matrícula (Fila 3)
        self._add_field(main_frame, 3, 0, "Grado:", self.grado_var, is_combo=True)
        self._add_field(main_frame, 3, 1, "Fecha Matrícula (YYYY-MM-DD):", self.fecha_matricula_var)

        # Campo Activa (Fila 4)
        ctk.CTkCheckBox(main_frame, text="Matrícula Activa", variable=self.activa_var, 
                        font=("Arial", 14)).grid(row=4, column=0, sticky="w", padx=20, pady=(10, 20))


        # Frame de Botones
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.grid(row=5, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")
        
        # Botones
        ctk.CTkButton(button_frame, text="➕ Crear Matrícula", command=self._handle_crear_matricula, height=45, 
                      fg_color="#2ecc71", hover_color="#27ae60", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", expand=True, fill="x", padx=5)
        
        self.btn_modificar = ctk.CTkButton(button_frame, text="✏️ Modificar", command=self._handle_actualizar_matricula, height=45, 
                      fg_color="#f39c12", hover_color="#e67e22", font=ctk.CTkFont(size=16, weight="bold"), state="disabled")
        self.btn_modificar.pack(side="left", expand=True, fill="x", padx=5)
        
        self.btn_eliminar = ctk.CTkButton(button_frame, text="🗑️ Eliminar", command=self._handle_eliminar_matricula, height=45, 
                      fg_color="#e74c3c", hover_color="#c0392b", font=ctk.CTkFont(size=16, weight="bold"), state="disabled")
        self.btn_eliminar.pack(side="left", expand=True, fill="x", padx=5)
        
        ctk.CTkButton(button_frame, text="🧹 Limpiar", command=self.limpiar_entradas, height=45, 
                      fg_color="#95a5a6", hover_color="#7f8c8d", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", expand=True, fill="x", padx=5)
        

    def _create_selection_widgets(self, parent, row_offset, label_text, var):
        """Crea la etiqueta y el ComboBox de NNA o Unidad Educativa."""
        ctk.CTkLabel(parent, text=label_text, font=("Arial", 14)).grid(row=row_offset*2, column=0, sticky="w", padx=20, pady=(20, 5))
        
        combo = ctk.CTkComboBox(parent, variable=var, values=["Cargando..."], height=40, width=300)
        combo.grid(row=row_offset*2 + 1, column=0, sticky="ew", padx=20, pady=(0, 10))
        
        # Vincular al evento de cambio para activar la búsqueda automática
        def _on_change(*args):
            # El evento se lanza incluso al establecer el valor inicial, por eso el filtro es clave.
            if var.get() not in ["Seleccionar NNA", "Seleccionar Unidad", "Cargando..."]:
                self._handle_buscar_matricula()
        
        var.trace_add("write", _on_change)
        
        if "NNA" in label_text:
            self.nna_combo = combo
        elif "Unidad" in label_text:
            self.unidad_combo = combo
            
    def _add_field(self, parent, row, column, label_text, var, is_combo=False):
        """Función auxiliar para añadir etiquetas y campos de entrada/combobox."""
        ctk.CTkLabel(parent, text=label_text, font=("Arial", 14)).grid(row=row, column=column, sticky="w", padx=20, pady=(10, 5))
        
        if is_combo:
            self.grado_combo = ctk.CTkComboBox(parent, variable=var, values=["Cargando..."], height=40)
            self.grado_combo.grid(row=row + 1, column=column, sticky="ew", padx=20, pady=(0, 10))
        else:
            ctk.CTkEntry(parent, textvariable=var, height=40).grid(row=row + 1, column=column, sticky="ew", padx=20, pady=(0, 10))


    # ----------------------------------------------------------------------
    # Métodos de Eventos (Delegación al Controlador)
    # ----------------------------------------------------------------------
    
    def _handle_crear_matricula(self):
        """Recolecta datos y delega la creación al controlador."""
        data = self._obtener_datos_formulario()
        self.controller.handle_crear_matricula(data)
            
    def _handle_buscar_matricula(self):
        """Busca la matrícula basada en la selección actual de NNA y Unidad."""
        nna_nombre = self.nna_var.get()
        unidad_nombre = self.unidad_var.get()
        
        nna_id = self.nna_map.get(nna_nombre)
        unidad_id = self.unidad_map.get(unidad_nombre)
        
        # Solo busca si ambos están seleccionados y son válidos
        if nna_id and unidad_id and nna_nombre not in ["Seleccionar NNA", "Cargando..."] and unidad_nombre not in ["Seleccionar Unidad", "Cargando..."]:
            self.controller.handle_buscar_matricula(nna_id, unidad_id)
        else:
             self.limpiar_entradas(clean_nna_unidad=False)
             self.display_message("Seleccione un NNA y una Unidad Educativa para buscar la matrícula existente.", is_success=True) 

            
    def _handle_actualizar_matricula(self):
        """Recolecta datos, verifica estado y delega la actualización al controlador."""
        if not self.matricula_cargada_id:
            self.display_message("❌ Primero debe buscar y cargar una matrícula para modificarla.", is_success=False)
            return

        data = self._obtener_datos_formulario()
        data['nna_id'] = self.matricula_cargada_id['nna_id']
        data['unidad_id'] = self.matricula_cargada_id['unidad_id']
        self.controller.handle_actualizar_matricula(data)
            
    def _handle_eliminar_matricula(self):
        """Verifica estado y delega la eliminación al controlador con confirmación."""
        if not self.matricula_cargada_id:
            self.display_message("❌ Primero debe buscar y cargar una matrícula para eliminarla.", is_success=False)
            return
            
        if messagebox.askyesno("⚠️ Confirmación", "¿Está seguro de que desea eliminar esta matrícula?"):
            self.controller.handle_eliminar_matricula(self.matricula_cargada_id['nna_id'], self.matricula_cargada_id['unidad_id'])
    
    # ----------------------------------------------------------------------
    # Métodos de Mutación de Vista (Llamados por el Controlador)
    # ----------------------------------------------------------------------

    def limpiar_entradas(self, clean_nna_unidad=True): 
        """Limpia los campos de matrícula y el estado de la matrícula cargada."""
        
        if clean_nna_unidad:
            self.nna_var.set("Seleccionar NNA")
            self.unidad_var.set("Seleccionar Unidad")
        
        grados_values = self.grado_combo.cget("values")
        self.grado_var.set(grados_values[0] if grados_values and grados_values[0] != "Cargando..." else "Seleccionar Grado")
        self.fecha_matricula_var.set(datetime.date.today().isoformat())
        self.activa_var.set(True)
        
        self.matricula_cargada_id = None
        self._set_btn_state("disabled")
        if self.message_label.cget("text") and not self.message_label.cget("text").startswith("Seleccione un NNA"):
             self.display_message("")


    def _obtener_datos_formulario(self): 
        """Recolecta los datos de los campos de entrada."""
        nna_nombre = self.nna_var.get()
        unidad_nombre = self.unidad_var.get()
        
        nna_id = self.nna_map.get(nna_nombre)
        unidad_id = self.unidad_map.get(unidad_nombre)
        
        return {
            "nna_id": nna_id, 
            "unidad_id": unidad_id,
            "grado": self.grado_var.get(),
            "fecha_matricula": self.fecha_matricula_var.get().strip(),
            "activa": self.activa_var.get()
        }
        
    def _establecer_datos_formulario(self, data: dict): 
        """Establece los valores de una matrícula cargada y habilita botones."""
        
        if 'nna_id' not in data or 'unidad_id' not in data:
            self.display_message("❌ Error: Datos de matrícula incompletos (falta ID de NNA/Unidad).", is_success=False)
            return

        self.grado_var.set(data.get("grado", ""))
        self.fecha_matricula_var.set(data.get("fecha_matricula", datetime.date.today().isoformat()))
        activa_db = data.get("activa", 0)
        self.activa_var.set(bool(activa_db)) 
        
        self.matricula_cargada_id = {'nna_id': data['nna_id'], 'unidad_id': data['unidad_id']}
        self._set_btn_state("normal")
        
    def _cargar_comboboxes(self, nna_list: List[Dict], unidad_list: List[Dict], grados_list: List[str]):
        """Carga las opciones en los ComboBoxes de NNA, Unidad y Grado."""
        
        # Cargar NNA
        nna_nombres = ["Seleccionar NNA"] + [n['nombre_completo'] for n in nna_list]
        self.nna_map = {n['nombre_completo']: n['id'] for n in nna_list}
        self.nna_combo.configure(values=nna_nombres)
        self.nna_var.set(nna_nombres[0])
        
        # Cargar Unidades
        unidad_nombres = ["Seleccionar Unidad"] + [u['nombre'] for u in unidad_list]
        self.unidad_map = {u['nombre']: u['id'] for u in unidad_list}
        self.unidad_combo.configure(values=unidad_nombres)
        self.unidad_var.set(unidad_nombres[0])
            
        # Cargar Grados
        if grados_list:
            self.grado_combo.configure(values=["Seleccionar Grado"] + grados_list)
            self.grado_var.set("Seleccionar Grado")
        else:
            self.grado_combo.configure(values=["Seleccionar Grado"])
            self.grado_var.set("Seleccionar Grado")

            
    def _set_btn_state(self, state):
        """Habilita o deshabilita los botones de Modificar/Eliminar."""
        self.btn_modificar.configure(state=state)
        self.btn_eliminar.configure(state=state)
        
    def display_message(self, message: str, is_success: bool = True):
        """Muestra un mensaje de estado en la interfaz."""
        color = "#2ecc71" if is_success else "#e74c3c"
        self.message_label.configure(text=message, text_color=color)