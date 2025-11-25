# views/funcion_vista_denuncia.py

import customtkinter as ctk
from tkinter import messagebox
from typing import Dict, List, Optional
import datetime

from controllers.denuncia_controller import DenunciaController
# Asumimos que también necesitarás controladores para buscar NNA, Personal y Persona general
# from controllers.nna_controller import NNAControlador
# from controllers.personal_controller import PersonalControlador
# from controllers.persona_controller import PersonaControlador # Para buscar denunciantes/denunciados

# ----------------------------------------------------------------------
# VISTA: GESTIÓN DE DENUNCIAS
# ----------------------------------------------------------------------

class DenunciaViewFrame(ctk.CTkFrame):
    """
    Vista para el módulo de gestión de Denuncias.
    Permite registrar, consultar, seguir y cerrar denuncias.
    """
    
    def __init__(self, master, controller: DenunciaController):
        super().__init__(master, corner_radius=0, fg_color="transparent") 
        
        self.controller = controller 
        
        self.denuncia_id_cargada: Optional[int] = None # ID de la denuncia actualmente cargada
        
        # Variables de control para la sección de Denuncia Principal
        self.buscar_denuncia_id_var = ctk.StringVar(self)
        self.consejero_id_var = ctk.StringVar(self)
        self.consejero_nombre_var = ctk.StringVar(self, value="Consejero no asignado")
        self.fecha_hechos_var = ctk.StringVar(self, value=datetime.date.today().isoformat())
        self.descripcion_denuncia_var = ctk.StringVar(self)
        self.estado_denuncia_var = ctk.StringVar(self, value="ACTIVA") # Solo para display

        # Variables para NNA Involucrados (usaremos una lista interna y una interfaz para añadir)
        self._nna_involucrados_temp: List[Dict] = []
        self.nna_involucrado_id_var = ctk.StringVar(self)
        self.nna_involucrado_nombre_var = ctk.StringVar(self, value="NNA no cargado")
        self.nna_involucrado_rol_var = ctk.StringVar(self, value="VICTIMA")
        self.nna_involucrado_detalle_var = ctk.StringVar(self)
        
        # Variables para Denunciantes (Lista interna y interfaz para añadir)
        self._denunciantes_temp: List[Dict] = []
        self.denunciante_id_var = ctk.StringVar(self) # Puede ser opcional (anónimo)
        self.denunciante_nombre_var = ctk.StringVar(self, value="Denunciante no cargado (o anónimo)")
        self.denunciante_declaracion_var = ctk.StringVar(self)
        self.denunciante_lesiones_var = ctk.StringVar(self)
        self.denunciante_anonimo_var = ctk.BooleanVar(self, value=False)

        # Variables para Denunciados (Lista interna y interfaz para añadir)
        self._denunciados_temp: List[int] = [] # Solo ID de persona
        self.denunciado_id_var = ctk.StringVar(self)
        self.denunciado_nombre_var = ctk.StringVar(self, value="Denunciado no cargado")

        # Variables para Seguimiento y Cierre
        self.seguimiento_consejero_id_var = ctk.StringVar(self)
        self.seguimiento_observaciones_var = ctk.StringVar(self)
        self.cierre_consejero_id_var = ctk.StringVar(self)
        self.cierre_acta_var = ctk.StringVar(self)
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1) 
        
        self._configurar_interfaz()

    # MÉTODO CLAVE: Requerido por la estructura de menu.py
    def show(self):
        """Llamado por MenuApp, invoca la carga de datos iniciales."""
        self.limpiar_todo()
        # Puedes cargar listas de consejeros aquí si las necesitas para los ComboBoxes
        # self._cargar_consejeros_disponibles()

    def _configurar_interfaz(self):
        """Configura la interfaz gráfica (Diseño General con Pestañas)."""
        
        self.title_label = ctk.CTkLabel(self, text="🚨 GESTIÓN DE DENUNCIAS", 
                                         font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="ew")

        self.message_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14), text_color="yellow")
        self.message_label.grid(row=1, column=0, pady=5, padx=20, sticky="ew")

        # Usar CTkTabview para organizar las secciones de la denuncia
        self.tabview = ctk.CTkTabview(self, width=800, height=600)
        self.tabview.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))

        # Pestaña 1: Denuncia Principal
        self.tabview.add("🔍 Denuncia Principal")
        self._configurar_tab_denuncia_principal(self.tabview.tab("🔍 Denuncia Principal"))
        
        # Pestaña 2: NNA Involucrados
        self.tabview.add("👶 NNA Involucrados")
        self._configurar_tab_nna_involucrados(self.tabview.tab("👶 NNA Involucrados"))

        # Pestaña 3: Denunciantes
        self.tabview.add("🗣️ Denunciantes")
        self._configurar_tab_denunciantes(self.tabview.tab("🗣️ Denunciantes"))

        # Pestaña 4: Denunciados
        self.tabview.add("😠 Denunciados")
        self._configurar_tab_denunciados(self.tabview.tab("😠 Denunciados"))

        # Pestaña 5: Seguimiento y Cierre
        self.tabview.add("📝 Seguimiento y Cierre")
        self._configurar_tab_seguimiento_cierre(self.tabview.tab("📝 Seguimiento y Cierre"))

        # Botón para registrar toda la denuncia (fuera de las pestañas)
        self.btn_registrar_denuncia_completa = ctk.CTkButton(self, text="✅ REGISTRAR DENUNCIA COMPLETA", command=self._handle_registrar_denuncia_completa,
                                                             height=50, fg_color="#2ecc71", hover_color="#27ae60", font=ctk.CTkFont(size=18, weight="bold"))
        self.btn_registrar_denuncia_completa.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
        
    def _configurar_tab_denuncia_principal(self, tab_frame: ctk.CTkFrame):
        tab_frame.columnconfigure(0, weight=1)
        tab_frame.rowconfigure(3, weight=1) # Para el textbox de descripción

        # Sección de Búsqueda
        search_frame = ctk.CTkFrame(tab_frame, fg_color="transparent")
        search_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
        search_frame.columnconfigure(0, weight=1)
        
        ctk.CTkLabel(search_frame, text="Buscar Denuncia (ID)", font=("Arial", 14)).grid(row=0, column=0, sticky="w", padx=10, pady=(5, 5))
        ctk.CTkEntry(search_frame, textvariable=self.buscar_denuncia_id_var, placeholder_text="ID de la Denuncia...", height=40).grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        ctk.CTkButton(search_frame, text="🔍 Cargar Denuncia", command=self._handle_cargar_denuncia, height=40,
                      fg_color="#3498db", hover_color="#2980b9").grid(row=1, column=1, padx=(10, 0), pady=(0, 10))
        
        # Frame para datos principales
        data_frame = ctk.CTkFrame(tab_frame, fg_color="transparent")
        data_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        data_frame.columnconfigure((0, 1), weight=1)
        
        self._add_field(data_frame, 0, 0, "ID Consejero Asignado:", self.consejero_id_var, tooltip="ID del personal que asigna la denuncia. Puedes buscarlo en el módulo de personal.")
        ctk.CTkLabel(data_frame, textvariable=self.consejero_nombre_var, text_color="#f1c40f").grid(row=1, column=1, sticky="w", padx=10) # Mostrar nombre del consejero
        
        self._add_field(data_frame, 2, 0, "Fecha de Hechos (YYYY-MM-DD):", self.fecha_hechos_var)
        
        ctk.CTkLabel(data_frame, text="Estado de la Denuncia:", font=("Arial", 14, "bold")).grid(row=2, column=1, sticky="w", padx=10, pady=(10, 5))
        ctk.CTkLabel(data_frame, textvariable=self.estado_denuncia_var, font=("Arial", 16, "bold"), text_color="#2ecc71").grid(row=3, column=1, sticky="w", padx=10, pady=(0, 5))

        # Descripción
        ctk.CTkLabel(tab_frame, text="Descripción de la Denuncia (Obligatoria):", font=("Arial", 14)).grid(row=2, column=0, sticky="w", padx=10, pady=(10, 5))
        self.descripcion_denuncia_textbox = ctk.CTkTextbox(tab_frame, wrap="word", height=150)
        self.descripcion_denuncia_textbox.grid(row=3, column=0, sticky="nsew", padx=10, pady=(0, 10))

    def _configurar_tab_nna_involucrados(self, tab_frame: ctk.CTkFrame):
        tab_frame.columnconfigure(0, weight=1)
        tab_frame.rowconfigure(1, weight=1)

        input_frame = ctk.CTkFrame(tab_frame, fg_color="transparent")
        input_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
        input_frame.columnconfigure((0, 1, 2), weight=1)

        self._add_field(input_frame, 0, 0, "ID NNA Involucrado:", self.nna_involucrado_id_var)
        ctk.CTkLabel(input_frame, textvariable=self.nna_involucrado_nombre_var, text_color="#3498db").grid(row=1, column=1, columnspan=2, sticky="w", padx=10)
        
        ctk.CTkButton(input_frame, text="Cargar NNA", command=self._handle_cargar_nna_involucrado, height=35).grid(row=0, column=1, sticky="ew", padx=(0, 5))

        self._add_field(input_frame, 2, 0, "Rol del NNA:", self.nna_involucrado_rol_var, is_combo=True, combo_values=self.controller.ROLES_NNA_VALIDOS)
        
        ctk.CTkLabel(input_frame, text="Detalle de Participación:", font=("Arial", 14)).grid(row=2, column=1, sticky="w", padx=10, pady=(10, 5))
        self.nna_detalle_textbox = ctk.CTkTextbox(input_frame, wrap="word", height=50)
        self.nna_detalle_textbox.grid(row=3, column=1, columnspan=2, sticky="ew", padx=10, pady=(0, 10))

        ctk.CTkButton(input_frame, text="➕ Añadir NNA a la Denuncia", command=self._handle_add_nna_involucrado, height=40,
                      fg_color="#3498db", hover_color="#2980b9").grid(row=4, column=0, columnspan=3, padx=10, pady=(10, 10), sticky="ew")

        # Listado de NNA involucrados ya añadidos
        ctk.CTkLabel(tab_frame, text="NNA Involucrados Actualmente:", font=("Arial", 16, "bold")).grid(row=1, column=0, sticky="w", padx=10, pady=(10, 5))
        self.listado_nna_involucrados = ctk.CTkTextbox(tab_frame, wrap="word", height=200, state="disabled")
        self.listado_nna_involucrados.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")
        
        ctk.CTkButton(tab_frame, text="❌ Limpiar NNA Involucrados Temporales", command=self._clear_nna_involucrados_temp, height=35).grid(row=3, column=0, padx=10, pady=(0, 10), sticky="ew")


    def _configurar_tab_denunciantes(self, tab_frame: ctk.CTkFrame):
        tab_frame.columnconfigure(0, weight=1)
        tab_frame.rowconfigure(1, weight=1)

        input_frame = ctk.CTkFrame(tab_frame, fg_color="transparent")
        input_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
        input_frame.columnconfigure((0, 1), weight=1)

        self._add_field(input_frame, 0, 0, "ID Denunciante (Vacío para Anónimo):", self.denunciante_id_var)
        ctk.CTkButton(input_frame, text="Cargar Persona", command=self._handle_cargar_denunciante, height=35).grid(row=0, column=1, sticky="ew", padx=(5, 0))
        ctk.CTkLabel(input_frame, textvariable=self.denunciante_nombre_var, text_color="#f1c40f").grid(row=1, column=0, columnspan=2, sticky="w", padx=10)
        
        ctk.CTkCheckBox(input_frame, text="Denunciante Anónimo", variable=self.denunciante_anonimo_var, command=self._toggle_denunciante_anonimo).grid(row=2, column=0, sticky="w", padx=10, pady=(10,5))
        
        ctk.CTkLabel(input_frame, text="Declaración (Obligatoria):", font=("Arial", 14)).grid(row=3, column=0, sticky="w", padx=10, pady=(10, 5))
        self.denunciante_declaracion_textbox = ctk.CTkTextbox(input_frame, wrap="word", height=70)
        self.denunciante_declaracion_textbox.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))

        ctk.CTkLabel(input_frame, text="Descripción de Lesiones (Opcional):", font=("Arial", 14)).grid(row=5, column=0, sticky="w", padx=10, pady=(10, 5))
        self.denunciante_lesiones_textbox = ctk.CTkTextbox(input_frame, wrap="word", height=50)
        self.denunciante_lesiones_textbox.grid(row=6, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))

        ctk.CTkButton(input_frame, text="➕ Añadir Denunciante a la Denuncia", command=self._handle_add_denunciante, height=40,
                      fg_color="#3498db", hover_color="#2980b9").grid(row=7, column=0, columnspan=2, padx=10, pady=(10, 10), sticky="ew")

        # Listado de Denunciantes ya añadidos
        ctk.CTkLabel(tab_frame, text="Denunciantes Actualmente:", font=("Arial", 16, "bold")).grid(row=1, column=0, sticky="w", padx=10, pady=(10, 5))
        self.listado_denunciantes = ctk.CTkTextbox(tab_frame, wrap="word", height=200, state="disabled")
        self.listado_denunciantes.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")
        
        ctk.CTkButton(tab_frame, text="❌ Limpiar Denunciantes Temporales", command=self._clear_denunciantes_temp, height=35).grid(row=3, column=0, padx=10, pady=(0, 10), sticky="ew")


    def _configurar_tab_denunciados(self, tab_frame: ctk.CTkFrame):
        tab_frame.columnconfigure(0, weight=1)
        tab_frame.rowconfigure(1, weight=1)

        input_frame = ctk.CTkFrame(tab_frame, fg_color="transparent")
        input_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
        input_frame.columnconfigure((0, 1), weight=1)

        self._add_field(input_frame, 0, 0, "ID Persona Denunciada:", self.denunciado_id_var)
        ctk.CTkButton(input_frame, text="Cargar Persona", command=self._handle_cargar_denunciado, height=35).grid(row=0, column=1, sticky="ew", padx=(5, 0))
        ctk.CTkLabel(input_frame, textvariable=self.denunciado_nombre_var, text_color="#e74c3c").grid(row=1, column=0, columnspan=2, sticky="w", padx=10)
        
        ctk.CTkButton(input_frame, text="➕ Añadir Denunciado a la Denuncia", command=self._handle_add_denunciado, height=40,
                      fg_color="#3498db", hover_color="#2980b9").grid(row=2, column=0, columnspan=2, padx=10, pady=(10, 10), sticky="ew")

        # Listado de Denunciados ya añadidos
        ctk.CTkLabel(tab_frame, text="Denunciados Actualmente:", font=("Arial", 16, "bold")).grid(row=1, column=0, sticky="w", padx=10, pady=(10, 5))
        self.listado_denunciados = ctk.CTkTextbox(tab_frame, wrap="word", height=200, state="disabled")
        self.listado_denunciados.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")
        
        ctk.CTkButton(tab_frame, text="❌ Limpiar Denunciados Temporales", command=self._clear_denunciados_temp, height=35).grid(row=3, column=0, padx=10, pady=(0, 10), sticky="ew")


    def _configurar_tab_seguimiento_cierre(self, tab_frame: ctk.CTkFrame):
        tab_frame.columnconfigure(0, weight=1)
        tab_frame.rowconfigure((1, 3), weight=1)

        # Sección de Seguimiento
        seguimiento_frame = ctk.CTkFrame(tab_frame, fg_color="#4a4a4a", corner_radius=10, label_text="AGREGAR SEGUIMIENTO")
        seguimiento_frame.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="ew")
        seguimiento_frame.columnconfigure(0, weight=1)
        
        self._add_field(seguimiento_frame, 0, 0, "ID Consejero (para Seguimiento):", self.seguimiento_consejero_id_var)
        ctk.CTkLabel(seguimiento_frame, text="Observaciones (Obligatorio):", font=("Arial", 14)).grid(row=2, column=0, sticky="w", padx=10, pady=(10, 5))
        self.seguimiento_observaciones_textbox = ctk.CTkTextbox(seguimiento_frame, wrap="word", height=100)
        self.seguimiento_observaciones_textbox.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))
        ctk.CTkButton(seguimiento_frame, text="➕ Registrar Seguimiento", command=self._handle_agregar_seguimiento, height=40,
                      fg_color="#27ae60", hover_color="#219c54").grid(row=4, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Sección de Cierre
        cierre_frame = ctk.CTkFrame(tab_frame, fg_color="#4a4a4a", corner_radius=10, label_text="CERRAR DENUNCIA")
        cierre_frame.grid(row=1, column=0, padx=10, pady=(10, 10), sticky="ew")
        cierre_frame.columnconfigure(0, weight=1)

        self._add_field(cierre_frame, 0, 0, "ID Consejero (para Cierre):", self.cierre_consejero_id_var)
        ctk.CTkLabel(cierre_frame, text="Acta de Cierre (Obligatoria):", font=("Arial", 14)).grid(row=2, column=0, sticky="w", padx=10, pady=(10, 5))
        self.cierre_acta_textbox = ctk.CTkTextbox(cierre_frame, wrap="word", height=100)
        self.cierre_acta_textbox.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))
        ctk.CTkButton(cierre_frame, text="🔒 Cerrar Denuncia", command=self._handle_cerrar_denuncia, height=40,
                      fg_color="#c0392b", hover_color="#a52e20").grid(row=4, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Listado de Seguimientos (cuando se cargue una denuncia)
        ctk.CTkLabel(tab_frame, text="Historial de Seguimientos:", font=("Arial", 16, "bold")).grid(row=2, column=0, sticky="w", padx=10, pady=(10, 5))
        self.listado_seguimientos = ctk.CTkTextbox(tab_frame, wrap="word", height=200, state="disabled")
        self.listado_seguimientos.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="nsew")

    def _add_field(self, parent, row, column, label_text, var, is_combo=False, combo_values=None, tooltip: Optional[str] = None):
        """Función auxiliar para añadir etiquetas y campos de entrada/combobox."""
        label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 14))
        label.grid(row=row, column=column, sticky="w", padx=10, pady=(10, 5))
        if tooltip:
            self._set_tooltip(label, tooltip) # Añadir tooltip
        
        if is_combo:
            combo = ctk.CTkComboBox(parent, variable=var, values=combo_values if combo_values else ["Cargando..."], height=40)
            combo.grid(row=row + 1, column=column, sticky="ew", padx=10, pady=(0, 5))
        else:
            ctk.CTkEntry(parent, textvariable=var, height=40).grid(row=row + 1, column=column, sticky="ew", padx=10, pady=(0, 5))

    def _set_tooltip(self, widget, text):
        """Crea un tooltip para el widget dado."""
        toolTip = ToolTip(widget, text) # Necesitas definir la clase ToolTip
        
    # ----------------------------------------------------------------------
    # Handlers de Eventos de Usuario
    # ----------------------------------------------------------------------

    def _handle_registrar_denuncia_completa(self):
        """
        Recopila todos los datos de las pestañas y llama al controlador para registrar la denuncia completa.
        """
        # Recopilar datos de Denuncia Principal
        datos_denuncia = {
            'consejero_id': self.consejero_id_var.get().strip(),
            'fecha_hechos': self.fecha_hechos_var.get().strip(),
            'descripcion': self.descripcion_denuncia_textbox.get("1.0", "end").strip()
        }
        
        # Validar consejero_id (debe ser numérico si no está vacío)
        if datos_denuncia['consejero_id']:
            try:
                datos_denuncia['consejero_id'] = int(datos_denuncia['consejero_id'])
            except ValueError:
                self.display_message("❌ El ID del Consejero debe ser un número entero.", is_success=False)
                return
        else:
            self.display_message("❌ El ID del Consejero es obligatorio para la denuncia principal.", is_success=False)
            return

        # Validar NNA Involucrados
        if not self._nna_involucrados_temp:
            self.display_message("❌ Debe añadir al menos un NNA involucrado.", is_success=False)
            return

        # Validar Denunciantes y Denunciados (al menos uno debe existir)
        if not self._denunciantes_temp and not self._denunciados_temp:
            self.display_message("❌ Debe añadir al menos un denunciante o un denunciado.", is_success=False)
            return

        exito, mensaje = self.controller.registrar_nueva_denuncia(
            datos_denuncia,
            self._nna_involucrados_temp,
            self._denunciantes_temp,
            self._denunciados_temp
        )
        
        self.display_message(mensaje, is_success=exito)
        if exito:
            self.limpiar_todo() # Limpiar todo al registrar con éxito

    def _handle_cargar_denuncia(self):
        """Carga los datos de una denuncia por su ID en todas las pestañas."""
        denuncia_id_str = self.buscar_denuncia_id_var.get().strip()
        if not denuncia_id_str.isdigit():
            self.display_message("❌ Ingrese un ID numérico para buscar la denuncia.", is_success=False)
            self.limpiar_todo(clean_search=False)
            return
        
        denuncia_id = int(denuncia_id_str)
        denuncia_data = self.controller.obtener_detalles_denuncia(denuncia_id)
        
        if denuncia_data:
            self.denuncia_id_cargada = denuncia_data['id']
            
            # Cargar datos en la pestaña principal
            self.consejero_id_var.set(str(denuncia_data.get('consejero_id', '')))
            self.consejero_nombre_var.set(denuncia_data.get('nombre_consejero', 'Desconocido'))
            self.fecha_hechos_var.set(denuncia_data.get('fecha_hechos', ''))
            self.descripcion_denuncia_textbox.delete("1.0", "end")
            self.descripcion_denuncia_textbox.insert("1.0", denuncia_data.get('descripcion', ''))
            self.estado_denuncia_var.set("ACTIVA" if denuncia_data.get('estado') else "CERRADA")
            self.display_message(f"✅ Denuncia ID {denuncia_id} cargada exitosamente.", is_success=True)
            
            # Aquí deberías llamar a métodos en el controlador para cargar
            # NNA involucrados, denunciantes, denunciados y seguimientos
            # asociados a esta denuncia_id y actualizar sus respectivas ListBoxes/Textboxes
            
            # --- SIMULACIÓN DE CARGA DE SUB-COMPONENTES (Reemplazar con llamadas reales) ---
            self._nna_involucrados_temp = [{"nna_id": 1, "rol": "VICTIMA", "detalle_participacion": "Detalle 1"}, {"nna_id": 2, "rol": "TESTIGO", "detalle_participacion": "Detalle 2"}]
            self._update_nna_involucrados_list()
            self._denunciantes_temp = [{"persona_id": 101, "declaracion": "Declaración X", "lesiones": "Ninguna"}]
            self._update_denunciantes_list()
            self._denunciados_temp = [201, 202]
            self._update_denunciados_list()
            # Faltaría cargar el historial de seguimientos
            # --- FIN SIMULACIÓN ---

        else:
            self.denuncia_id_cargada = None
            self.display_message(f"❌ Denuncia ID {denuncia_id} no encontrada.", is_success=False)
            self.limpiar_todo(clean_search=False) # Limpiar solo el resto del formulario


    # --- Handlers para añadir NNA, Denunciantes, Denunciados (temporalmente a listas internas) ---
    def _handle_cargar_nna_involucrado(self):
        nna_id_str = self.nna_involucrado_id_var.get().strip()
        if not nna_id_str.isdigit():
            self.display_message("❌ Ingrese un ID numérico para el NNA.", is_success=False)
            return
        
        nna_id = int(nna_id_str)
        # Aquí llamarías a nna_controller.obtener_nna_por_id(nna_id)
        # Simulación
        nombre_nna = f"NNA {nna_id} (Simulado)" 
        self.nna_involucrado_nombre_var.set(nombre_nna)
        self.display_message(f"NNA ID {nna_id} cargado.", is_success=True)

    def _handle_add_nna_involucrado(self):
        nna_id_str = self.nna_involucrado_id_var.get().strip()
        rol = self.nna_involucrado_rol_var.get().strip()
        detalle = self.nna_detalle_textbox.get("1.0", "end").strip()

        if not nna_id_str or not rol:
            self.display_message("❌ ID de NNA y Rol son obligatorios.", is_success=False)
            return
        
        try:
            nna_id = int(nna_id_str)
        except ValueError:
            self.display_message("❌ El ID del NNA debe ser un número entero.", is_success=False)
            return

        # Verificar si el NNA ya fue añadido
        if any(n['nna_id'] == nna_id for n in self._nna_involucrados_temp):
            self.display_message(f"⚠️ El NNA ID {nna_id} ya ha sido añadido. Elimínelo primero para modificarlo.", is_success=False)
            return
        
    def _handle_add_nna_involucrado(self):
        nna_id_str = self.nna_involucrado_id_var.get().strip()
        rol = self.nna_involucrado_rol_var.get().strip()
        detalle = self.nna_detalle_textbox.get("1.0", "end").strip()

        if not nna_id_str or not rol:
            self.display_message("❌ ID de NNA y Rol son obligatorios.", is_success=False)
            return
        
        try:
            nna_id = int(nna_id_str)
        except ValueError:
            self.display_message("❌ El ID del NNA debe ser un número entero.", is_success=False)
            return

        # Verificar si el NNA ya fue añadido
        if any(n['nna_id'] == nna_id for n in self._nna_involucrados_temp):
            self.display_message(f"⚠️ El NNA ID {nna_id} ya ha sido añadido. Elimínelo primero para modificarlo.", is_success=False)
            return
        
        # Añadir a la lista temporal
        self._nna_involucrados_temp.append({
            'nna_id': nna_id,
            'rol': rol,
            'detalle_participacion': detalle if detalle else None
        })
        
        self._update_nna_involucrados_list()
        
        # Limpiar formulario de adición
        self.nna_involucrado_id_var.set("")
        self.nna_involucrado_nombre_var.set("NNA no cargado")
        self.nna_detalle_textbox.delete("1.0", "end")
        self.display_message(f"✅ NNA ID {nna_id} añadido temporalmente a la denuncia.", is_success=True)

    def _update_nna_involucrados_list(self):
        """Actualiza el widget de texto con la lista de NNA involucrados temporales."""
        self.listado_nna_involucrados.configure(state="normal")
        self.listado_nna_involucrados.delete("1.0", "end")
        
        if not self._nna_involucrados_temp:
            self.listado_nna_involucrados.insert("end", "No hay NNA involucrados añadidos temporalmente.")
        else:
            header = "{:<10} {:<15} {:<50}\n".format("ID NNA", "ROL", "DETALLE")
            self.listado_nna_involucrados.insert("end", header, "header")
            self.listado_nna_involucrados.insert("end", "-" * 75 + "\n")
            
            for nna in self._nna_involucrados_temp:
                linea = "{:<10} {:<15} {:<50}\n".format(
                    nna['nna_id'], 
                    nna['rol'], 
                    nna['detalle_participacion'][:45] + '...' if nna['detalle_participacion'] and len(nna['detalle_participacion']) > 45 else nna['detalle_participacion'] or 'N/A'
                )
                self.listado_nna_involucrados.insert("end", linea)

        self.listado_nna_involucrados.configure(state="disabled")

    def _clear_nna_involucrados_temp(self):
        """Limpia la lista temporal de NNA involucrados."""
        self._nna_involucrados_temp = []
        self._update_nna_involucrados_list()
        self.display_message("🧹 Lista de NNA involucrados temporales limpiada.", is_success=True)

    def _toggle_denunciante_anonimo(self):
        """Habilita/deshabilita el campo de ID del denunciante si es anónimo."""
        is_anonimo = self.denunciante_anonimo_var.get()
        state = "disabled" if is_anonimo else "normal"
        # Esto requeriría acceder al widget Entry, que no se guardó en _add_field. 
        # Una solución rápida es limpiar la variable.
        if is_anonimo:
            self.denunciante_id_var.set("")
            self.denunciante_nombre_var.set("Denunciante Anónimo")
        else:
            self.denunciante_nombre_var.set("Denunciante no cargado (o anónimo)")


    def _handle_cargar_denunciante(self):
        persona_id_str = self.denunciante_id_var.get().strip()
        if not persona_id_str.isdigit():
            self.display_message("❌ Ingrese un ID numérico para el Denunciante.", is_success=False)
            return
        
        persona_id = int(persona_id_str)
        # Aquí llamarías a persona_controller.obtener_persona_por_id(persona_id)
        # Simulación
        nombre_persona = f"Persona {persona_id} (Simulado)" 
        self.denunciante_nombre_var.set(nombre_persona)
        self.denunciante_anonimo_var.set(False)
        self.display_message(f"Persona ID {persona_id} cargada como denunciante.", is_success=True)

    def _handle_add_denunciante(self):
        persona_id_str = self.denunciante_id_var.get().strip()
        declaracion = self.denunciante_declaracion_textbox.get("1.0", "end").strip()
        lesiones = self.denunciante_lesiones_textbox.get("1.0", "end").strip()
        es_anonimo = self.denunciante_anonimo_var.get()

        if not declaracion or len(declaracion) < 10:
            self.display_message("❌ La declaración del denunciante es obligatoria y debe ser descriptiva.", is_success=False)
            return

        persona_id = None
        if not es_anonimo:
            try:
                persona_id = int(persona_id_str)
            except ValueError:
                self.display_message("❌ El ID de la Persona (no anónima) debe ser un número entero.", is_success=False)
                return

        # Añadir a la lista temporal
        self._denunciantes_temp.append({
            'persona_id': persona_id,
            'declaracion': declaracion,
            'lesiones': lesiones if lesiones else None
        })
        
        self._update_denunciantes_list()
        
        # Limpiar formulario de adición
        self.denunciante_id_var.set("")
        self.denunciante_nombre_var.set("Denunciante no cargado (o anónimo)")
        self.denunciante_declaracion_textbox.delete("1.0", "end")
        self.denunciante_lesiones_textbox.delete("1.0", "end")
        self.denunciante_anonimo_var.set(False)
        self.display_message("✅ Denunciante añadido temporalmente a la denuncia.", is_success=True)

    def _update_denunciantes_list(self):
        """Actualiza el widget de texto con la lista de denunciantes temporales."""
        self.listado_denunciantes.configure(state="normal")
        self.listado_denunciantes.delete("1.0", "end")
        
        if not self._denunciantes_temp:
            self.listado_denunciantes.insert("end", "No hay denunciantes añadidos temporalmente.")
        else:
            header = "{:<10} {:<30} {:<30}\n".format("ID PERS", "DECLARACIÓN", "LESIÓN")
            self.listado_denunciantes.insert("end", header, "header")
            self.listado_denunciantes.insert("end", "-" * 75 + "\n")
            
            for d in self._denunciantes_temp:
                id_str = str(d['persona_id']) if d['persona_id'] else 'ANÓNIMO'
                linea = "{:<10} {:<30} {:<30}\n".format(
                    id_str, 
                    d['declaracion'][:25] + '...' if len(d['declaracion']) > 25 else d['declaracion'],
                    d['lesiones'][:25] + '...' if d['lesiones'] and len(d['lesiones']) > 25 else d['lesiones'] or 'N/A'
                )
                self.listado_denunciantes.insert("end", linea)

        self.listado_denunciantes.configure(state="disabled")

    def _clear_denunciantes_temp(self):
        """Limpia la lista temporal de Denunciantes."""
        self._denunciantes_temp = []
        self._update_denunciantes_list()
        self.display_message("🧹 Lista de denunciantes temporales limpiada.", is_success=True)

    def _handle_cargar_denunciado(self):
        persona_id_str = self.denunciado_id_var.get().strip()
        if not persona_id_str.isdigit():
            self.display_message("❌ Ingrese un ID numérico para el Denunciado.", is_success=False)
            return
        
        persona_id = int(persona_id_str)
        # Aquí llamarías a persona_controller.obtener_persona_por_id(persona_id)
        # Simulación
        nombre_persona = f"Persona {persona_id} (Simulado)" 
        self.denunciado_nombre_var.set(nombre_persona)
        self.display_message(f"Persona ID {persona_id} cargada como denunciado.", is_success=True)

    def _handle_add_denunciado(self):
        persona_id_str = self.denunciado_id_var.get().strip()

        if not persona_id_str:
            self.display_message("❌ El ID del Denunciado es obligatorio.", is_success=False)
            return
        
        try:
            persona_id = int(persona_id_str)
        except ValueError:
            self.display_message("❌ El ID del Denunciado debe ser un número entero.", is_success=False)
            return

        if persona_id in self._denunciados_temp:
            self.display_message(f"⚠️ El Denunciado ID {persona_id} ya ha sido añadido.", is_success=False)
            return

        # Añadir a la lista temporal
        self._denunciados_temp.append(persona_id)
        
        self._update_denunciados_list()
        
        # Limpiar formulario de adición
        self.denunciado_id_var.set("")
        self.denunciado_nombre_var.set("Denunciado no cargado")
        self.display_message(f"✅ Denunciado ID {persona_id} añadido temporalmente a la denuncia.", is_success=True)

    def _update_denunciados_list(self):
        """Actualiza el widget de texto con la lista de denunciados temporales."""
        self.listado_denunciados.configure(state="normal")
        self.listado_denunciados.delete("1.0", "end")
        
        if not self._denunciados_temp:
            self.listado_denunciados.insert("end", "No hay denunciados añadidos temporalmente.")
        else:
            header = "{:<10} {:<30}\n".format("ID PERS", "NOMBRE SIMULADO")
            self.listado_denunciados.insert("end", header, "header")
            self.listado_denunciados.insert("end", "-" * 40 + "\n")
            
            for p_id in self._denunciados_temp:
                # En la vista final, buscarías el nombre real de la persona
                nombre_simulado = f"Persona ID {p_id}" 
                linea = "{:<10} {:<30}\n".format(p_id, nombre_simulado)
                self.listado_denunciados.insert("end", linea)

        self.listado_denunciados.configure(state="disabled")

    def _clear_denunciados_temp(self):
        """Limpia la lista temporal de Denunciados."""
        self._denunciados_temp = []
        self._update_denunciados_list()
        self.display_message("🧹 Lista de denunciados temporales limpiada.", is_success=True)

    # ----------------------------------------------------------------------
    # Handlers de Seguimiento y Cierre
    # ----------------------------------------------------------------------

    def _handle_agregar_seguimiento(self):
        if not self.denuncia_id_cargada:
            self.display_message("❌ Debe cargar una denuncia existente para agregar seguimiento.", is_success=False)
            return
        
        consejero_id_str = self.seguimiento_consejero_id_var.get().strip()
        observaciones = self.seguimiento_observaciones_textbox.get("1.0", "end").strip()

        if not consejero_id_str.isdigit():
            self.display_message("❌ ID del Consejero para seguimiento debe ser un número.", is_success=False)
            return

        exito, mensaje = self.controller.agregar_registro_seguimiento(
            self.denuncia_id_cargada,
            int(consejero_id_str),
            observaciones
        )
        
        self.display_message(mensaje, is_success=exito)
        if exito:
            self.seguimiento_observaciones_textbox.delete("1.0", "end")
            # Debería recargar el historial de seguimientos (método no implementado)
            
    def _handle_cerrar_denuncia(self):
        if not self.denuncia_id_cargada:
            self.display_message("❌ Debe cargar una denuncia existente para cerrarla.", is_success=False)
            return
            
        if self.estado_denuncia_var.get() == "CERRADA":
            self.display_message("⚠️ Esta denuncia ya está cerrada.", is_success=False)
            return

        consejero_id_str = self.cierre_consejero_id_var.get().strip()
        acta_cierre = self.cierre_acta_textbox.get("1.0", "end").strip()
        
        if not consejero_id_str.isdigit():
            self.display_message("❌ ID del Consejero para cierre debe ser un número.", is_success=False)
            return

        if messagebox.askyesno("⚠️ Confirmar Cierre", f"¿Está seguro de cerrar la Denuncia ID {self.denuncia_id_cargada}? Esta acción es permanente."):
            exito, mensaje = self.controller.cerrar_expediente_denuncia(
                self.denuncia_id_cargada,
                int(consejero_id_str),
                acta_cierre
            )
            
            self.display_message(mensaje, is_success=exito)
            if exito:
                self.estado_denuncia_var.set("CERRADA")

    # ----------------------------------------------------------------------
    # Métodos de Mutación de Vista
    # ----------------------------------------------------------------------

    def limpiar_todo(self, clean_search=True): 
        """Limpia todos los campos del formulario de denuncia."""
        if clean_search: self.buscar_denuncia_id_var.set("")
        
        # Limpieza Pestaña Principal
        self.consejero_id_var.set("")
        self.consejero_nombre_var.set("Consejero no asignado")
        self.fecha_hechos_var.set(datetime.date.today().isoformat())
        self.descripcion_denuncia_textbox.delete("1.0", "end")
        self.estado_denuncia_var.set("ACTIVA")
        self.denuncia_id_cargada = None
        
        # Limpieza Temporal (Listas)
        self._clear_nna_involucrados_temp()
        self._clear_denunciantes_temp()
        self._clear_denunciados_temp()

        # Limpieza Seguimiento/Cierre
        self.seguimiento_observaciones_textbox.delete("1.0", "end")
        self.cierre_acta_textbox.delete("1.0", "end")
        self.listado_seguimientos.configure(state="normal")
        self.listado_seguimientos.delete("1.0", "end")
        self.listado_seguimientos.configure(state="disabled")

        self.display_message("")
        
    def display_message(self, message: str, is_success: bool = True):
        """Muestra un mensaje de estado en la interfaz."""
        color = "#2ecc71" if is_success else "#e74c3c"
        self.message_label.configure(text=message, text_color=color)

# NOTA: Se requiere la definición de la clase ToolTip si se usa self._set_tooltip.

class ToolTip:
    """
    Clase para crear tooltips en Tkinter.
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     # milisegundos
        self.wraplength = 180   # píxeles
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id_ = self.id
        self.id = None
        if id_:
            self.widget.after_cancel(id_)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # crea una ventana toplevel
        self.tw = ctk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)  # elimina la barra de título
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = ctk.Label(self.tw, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         wraplength=self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()
# Se omite aquí por brevedad, pero es una clase estándar de Tkinter.