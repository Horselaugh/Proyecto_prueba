import customtkinter as ctk
from tkinter import messagebox
from typing import List, Optional, Dict, Any
from datetime import date
from datetime import datetime

# ======================================================================
# MOCK del Controlador (Definición movida para evitar 'not defined' error)
# Esto garantiza que el nombre 'MockControlador' esté siempre disponible, 
# incluso si la importación del controlador real tiene éxito.
# ======================================================================
class MockControlador:
    def __init__(self): self.vista = None
    def set_view(self, view_instance): self.vista = view_instance
    def load_initial_data(self):
        if self.vista:
            self.vista._cargar_opciones_expedientes(["10 - Caso NNA Juan P. (Abierto)", "15 - Caso NNA María L. (Abierto)"])
            self.vista.display_message("Mock: Datos iniciales cargados. Genere el historial.", True)
    def handle_registrar_seguimiento(self, exp_str, comentario):
        self.vista.display_message("Mock: Seguimiento registrado.", True)
        self.vista.limpiar_registro()
        self.handle_listar_seguimientos(expediente_id=10) # Para refrescar
    def handle_listar_seguimientos(self, expediente_id=None, desde=None, hasta=None):
        self.vista._mostrar_historial([
            {"id": 1, "expediente_id": 10, "expediente_desc": "10 - Caso NNA Juan P. (Abierto)", "comentario": "Evaluación inicial de caso.", "fecha": "2024-10-01", "creado_en": "2024-10-01 10:00:00"},
            {"id": 2, "expediente_id": 15, "expediente_desc": "15 - Caso NNA María L. (Abierto)", "comentario": "Alerta de riesgo activada.", "fecha": "2024-10-10", "creado_en": "2024-10-10 09:00:00"},
        ], message="Historial cargado (Mock)")
    def get_expediente_id_from_str(self, exp_str: str) -> Optional[int]:
        return 10 if exp_str.startswith("10") else 15

# Importamos el controlador (o su mock)
try:
    from controllers.seguimiento_expediente_controllers import SeguimientoExpedienteControlador
except ImportError:
    # Si la importación falla, asignamos el MockControlador
    SeguimientoExpedienteControlador = MockControlador


class SeguimientoExpedienteViewFrame(ctk.CTkFrame):
    """
    Vista para el módulo de Seguimiento de Expedientes.
    Hereda de CTkFrame para ser cargado en el panel de contenido (MenuApp).
    """

    # Usamos 'Any' para la anotación de tipo del controlador, 
    # ya que podría ser SeguimientoExpedienteControlador (si existe) o MockControlador.
    def __init__(self, master, controller: MockControlador): 
        super().__init__(master, corner_radius=0, fg_color="transparent") 
        
        self.controller = controller 
        self.controller.set_view(self) 
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1) 
        
        # Variables de control
        self.expediente_var = ctk.StringVar(self, value="Seleccionar Expediente")
        self.filtro_exp_var = ctk.StringVar(self, value="Todos")
        self.filtro_desde_var = ctk.StringVar(self, value="")
        self.filtro_hasta_var = ctk.StringVar(self, value="")
        
        self._configurar_interfaz()

    def show(self):
        """Llamado por MenuApp, invoca la carga de datos iniciales del controlador."""
        self.controller.load_initial_data() 

    def _configurar_interfaz(self):
        """Configura la interfaz gráfica (Diseño General con pestañas)."""
        
        # Título y Mensaje
        self.title_label = ctk.CTkLabel(self, text="📝 SEGUIMIENTO DE EXPEDIENTES", 
                                        font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="ew")

        self.message_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14), text_color="yellow")
        self.message_label.grid(row=1, column=0, pady=5, padx=20, sticky="ew")

        # Tabview para Registro y Historial
        self.tabview = ctk.CTkTabview(self, fg_color="#3c3c3c", segmented_button_selected_color="#3498db")
        self.tabview.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        self.tabview.add("✍️ Registrar Seguimiento")
        self.tabview.add("📜 Historial de Seguimientos")
        
        self.tabview.tab("✍️ Registrar Seguimiento").columnconfigure(0, weight=1)
        self.tabview.tab("📜 Historial de Seguimientos").columnconfigure(0, weight=1)
        self.tabview.tab("📜 Historial de Seguimientos").rowconfigure(1, weight=1)
        
        self._crear_tab_registro()
        self._crear_tab_historial()
        
    def _crear_tab_registro(self):
        tab = self.tabview.tab("✍️ Registrar Seguimiento")
        
        registro_frame = ctk.CTkFrame(tab, fg_color="transparent")
        registro_frame.pack(fill="both", expand=True, padx=20, pady=20)
        registro_frame.columnconfigure(0, weight=1)
        registro_frame.rowconfigure(2, weight=1) # El campo de texto crece

        # Selector de Expediente
        ctk.CTkLabel(registro_frame, text="Expediente (Obligatorio):", font=("Arial", 14)).grid(row=0, column=0, sticky="w", padx=10, pady=(0, 5))
        self.exp_combo = ctk.CTkComboBox(registro_frame, 
                                            variable=self.expediente_var, 
                                            values=["Cargando..."],
                                            height=40)
        self.exp_combo.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))

        # Comentario
        ctk.CTkLabel(registro_frame, text="Comentario / Descripción del Seguimiento (Mín. 10 caracteres):", font=("Arial", 14)).grid(row=2, column=0, sticky="w", padx=10, pady=(0, 5))
        self.comentario_textbox = ctk.CTkTextbox(registro_frame, height=200, font=("Arial", 14))
        self.comentario_textbox.grid(row=3, column=0, sticky="nsew", padx=10, pady=(0, 15))

        # Botón de Registro
        ctk.CTkButton(registro_frame, text="➕ Registrar Seguimiento", command=self._handle_registrar, 
                      fg_color="#2ecc71", hover_color="#27ae60", height=45, 
                      font=ctk.CTkFont(size=16, weight="bold")).grid(row=4, column=0, sticky="ew", padx=10, pady=(5, 10))


    def _crear_tab_historial(self):
        tab = self.tabview.tab("📜 Historial de Seguimientos")
        
        # Frame de Filtros
        filtro_frame = ctk.CTkFrame(tab, fg_color="#2e2e2e")
        filtro_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(10, 5))

        # Expediente a filtrar
        ctk.CTkLabel(filtro_frame, text="Expediente:", anchor="w").grid(row=0, column=0, padx=(10, 5), pady=6, sticky="w")
        self.filtro_exp_combo = ctk.CTkComboBox(filtro_frame, 
                                                variable=self.filtro_exp_var, 
                                                values=["Todos", "Cargando..."],
                                                height=35)
        self.filtro_exp_combo.grid(row=0, column=1, padx=5, pady=6, sticky="ew")

        # Fecha Desde
        ctk.CTkLabel(filtro_frame, text="Desde (YYYY-MM-DD):", anchor="w").grid(row=0, column=2, padx=(15, 5), pady=6, sticky="w")
        ctk.CTkEntry(filtro_frame, textvariable=self.filtro_desde_var, placeholder_text="Ej: 2024-01-01", height=35).grid(row=0, column=3, padx=5, pady=6, sticky="ew")

        # Fecha Hasta
        ctk.CTkLabel(filtro_frame, text="Hasta (YYYY-MM-DD):", anchor="w").grid(row=0, column=4, padx=(15, 5), pady=6, sticky="w")
        ctk.CTkEntry(filtro_frame, textvariable=self.filtro_hasta_var, placeholder_text=date.today().strftime("%Y-%m-%d"), height=35).grid(row=0, column=5, padx=5, pady=6, sticky="ew")
        
        # Botón de Filtro
        ctk.CTkButton(filtro_frame, text="🔍 Filtrar", command=self._handle_listar_seguimientos, 
                      fg_color="#3498db", hover_color="#2980b9", height=35).grid(row=0, column=6, padx=(10, 10), pady=6)
                      
        # Contenedor de Resultados
        self.resultados_frame = ctk.CTkScrollableFrame(tab, label_text="HISTORIAL DE SEGUIMIENTOS", fg_color="#2e2e2e")
        self.resultados_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(5, 20))
        self.resultados_frame.columnconfigure(0, weight=1)

    # ----------------------------------------------------------------------
    # Métodos de Eventos (Delegación al Controlador)
    # ----------------------------------------------------------------------

    def _handle_registrar(self):
        """Recoge los datos del formulario de registro y llama al controlador."""
        exp_str = self.expediente_var.get()
        comentario = self.comentario_textbox.get("1.0", "end-1c").strip()
        
        if exp_str == "Seleccionar Expediente":
            self.display_message("❌ Debe seleccionar un Expediente.", is_success=False)
            return

        self.controller.handle_registrar_seguimiento(exp_str, comentario)

    def _handle_listar_seguimientos(self):
        """Recoge los datos del formulario de historial y llama al controlador."""
        exp_str = self.filtro_exp_var.get()
        exp_id = None
        if exp_str != "Todos":
            exp_id = self.controller.get_expediente_id_from_str(exp_str)

        desde = self.filtro_desde_var.get().strip() or None
        hasta = self.filtro_hasta_var.get().strip() or None

        self.controller.handle_listar_seguimientos(expediente_id=exp_id, desde=desde, hasta=hasta)

    # ----------------------------------------------------------------------
    # Métodos de Mutación de Vista (Llamados por el Controlador)
    # ----------------------------------------------------------------------

    def _cargar_opciones_expedientes(self, opciones: List[str]):
        """Carga las opciones disponibles en los ComboBoxes de Expedientes."""
        if opciones:
            # ComboBox de Registro
            self.exp_combo.configure(values=opciones)
            self.expediente_var.set(opciones[0]) 
            
            # ComboBox de Filtro (incluyendo "Todos")
            opciones_filtro = ["Todos"] + opciones
            self.filtro_exp_combo.configure(values=opciones_filtro)
            self.filtro_exp_var.set("Todos") 
        
    def _mostrar_historial(self, filas: List[Dict], message: Optional[str] = None):
        """Muestra la lista de seguimientos en el frame de resultados del historial."""
        
        # Limpiar frame anterior
        for w in self.resultados_frame.winfo_children():
            w.destroy()
            
        if message:
             # Mostrar el mensaje de estado (éxito o error)
             ctk.CTkLabel(self.resultados_frame, text=message, font=("Arial", 14), 
                          text_color="#e74c3c" if "Error" in message or "No hay" in message else "#2ecc71").pack(pady=12, padx=10)
             if not filas: return

        if not filas:
            ctk.CTkLabel(self.resultados_frame, text="No hay registros para los parámetros indicados.", font=("Arial", 14)).pack(pady=12, padx=10)
            return

        for idx, r in enumerate(filas):
            exp_desc = r.get('expediente_desc', f"EXP {r['expediente_id']}")
            # Formatear la fecha para mejor legibilidad
            fecha_reg = datetime.strptime(r['creado_en'][:10], '%Y-%m-%d').strftime('%d-%m-%Y')
            
            texto = (
                f"ID Seguimiento: {r['id']} | Expediente: {exp_desc}\n"
                f"Fecha del Seguimiento: {r['fecha']} | Registrado: {fecha_reg}\n"
                f"Comentario: {r['comentario']}"
            )
            
            lbl = ctk.CTkLabel(
                self.resultados_frame, 
                text=texto, 
                anchor="w", 
                justify="left",
                fg_color="#2c3e50" if idx % 2 == 0 else "#34495e",
                corner_radius=8,
                wraplength=750,
                padx=10,
                pady=10
            )
            lbl.pack(fill="x", padx=10, pady=(6 if idx==0 else 3,3))

    def limpiar_registro(self):
        """Limpia los campos del formulario de registro."""
        if self.exp_combo.cget("values"): 
            self.expediente_var.set(self.exp_combo.cget("values")[0])
        self.comentario_textbox.delete("1.0", "end")
        
    def display_message(self, message: str, is_success: bool = True):
        """Muestra un mensaje de estado en la interfaz."""
        color = "#2ecc71" if is_success else "#e74c3c"
        self.message_label.configure(text=message, text_color=color)