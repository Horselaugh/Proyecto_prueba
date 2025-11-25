import customtkinter as ctk
from tkinter import messagebox
from typing import Dict, List, Optional
import datetime

# ----------------------------------------------------------------------
# MOCK DE MODELO (TEMPORAL) - ACTUALIZADO
# ----------------------------------------------------------------------
class MockPersonalModel:
    def obtener_por_id(self, id):
        if id == 1:
            # La Vista espera estos campos ya procesados por el Controlador
            return {
                "id": 1, 
                "documento_identidad": "V12345678", # Clave correcta para la cédula
                "primer_nombre": "Juan", 
                "segundo_nombre": "Carlos", # Añadido
                "primer_apellido": "Pérez", 
                "segundo_apellido": "Rojas", # Añadido
                "telefono": "04141234567",
                "direccion": "Calle Falsa 123", # Añadido
                "genero": "Masculino", # Nombre completo (mapeado por Controller)
                "cargo_id": 1, 
                "nombre_usuario": "jperez", # Añadido
                "resolucion": "N/A"
            }
        return None
        
    def obtener_por_cedula(self, cedula): # Añadido para consistencia
        if cedula == "V12345678":
            return self.obtener_por_id(1)
        return None

    def agregar_personal(self, datos): return 2 
    # El método actualizar_personal de la vista MOCK recibe 'data'
    def actualizar_personal(self, data): return True 
    def eliminar_personal(self, id): return True 
    
    def listar_generos(self): return ["Femenino", "Masculino", "Otro"]
    def listar_cargos(self): return [{"id": 1, "nombre": "Coordinador"}, {"id": 2, "nombre": "Secretario"}]

# ----------------------------------------------------------------------
# MOCK DE CONTROLADOR (Necesario para la Vista si se ejecuta sola) - AJUSTADO
# ----------------------------------------------------------------------
class PersonalControlador:
    def __init__(self):
        self.modelo = MockPersonalModel() 
        self.vista = None
        self.cargo_map: Dict[str, int] = {}
        self.genero_map: Dict[str, str] = {"Femenino": "F", "Masculino": "M", "Otro": "O"}

    def set_view(self, view_instance): self.vista = view_instance
        
    def load_initial_data(self):
        cargos = self.modelo.listar_cargos()
        generos = self.modelo.listar_generos()
        self.cargo_map = {c['nombre']: c['id'] for c in cargos}
        self.vista._cargar_cargos([c['nombre'] for c in cargos])
        self.vista._cargar_generos(generos)
        self.vista.display_message("Listo para gestionar Personal. Ingrese ID/Cédula para buscar. 🔎", is_success=True)

    def handle_crear_personal(self, *args): self.vista.display_message("Mock: Crear Personal", True)
    
    def handle_cargar_personal(self, id_or_cedula): 
        resultado = self.modelo.obtener_por_id(1) # Siempre carga el mock ID 1
        if resultado:
            # Simular mapeo de cargo (el controlador real lo haría)
            cargo_nombre = next((c['nombre'] for c, i in self.cargo_map.items() if i == resultado['cargo_id']), "Desconocido")
            resultado['cargo_nombre'] = cargo_nombre
            
            self.vista._establecer_datos_formulario(resultado)
            self.vista.display_message("Mock: Personal cargado (ID 1)", True)
        else:
            self.vista.display_message("Mock: Personal no encontrado", False)
            self.vista.limpiar_entradas(clean_search=False)
            
    def handle_actualizar_personal(self, *args): self.vista.display_message("Mock: Actualizar Personal", True)
    def handle_eliminar_personal(self, *args): self.vista.display_message("Mock: Eliminar Personal", True)


# ----------------------------------------------------------------------
# CLASE DE VISTA ADAPTADA
# ----------------------------------------------------------------------

class PersonalViewFrame(ctk.CTkFrame):
    """
    Vista para el módulo de gestión de Personal. 
    Hereda de CTkFrame.
    """
    
    def __init__(self, master, controller: PersonalControlador):
        super().__init__(master, corner_radius=0, fg_color="transparent") 
        
        self.controller = controller 
        self.controller.set_view(self) 
        
        self.personal_id_cargado: Optional[int] = None
        
        # Variables de control
        self.buscar_var = ctk.StringVar(self)
        self.cedula_var = ctk.StringVar(self)
        self.p_nombre_var = ctk.StringVar(self)
        self.s_nombre_var = ctk.StringVar(self)
        self.p_apellido_var = ctk.StringVar(self)
        self.s_apellido_var = ctk.StringVar(self)
        self.telefono_var = ctk.StringVar(self)
        self.direccion_var = ctk.StringVar(self)
        self.genero_var = ctk.StringVar(self, value="Seleccionar Género")
        self.cargo_var = ctk.StringVar(self, value="Seleccionar Cargo")
        self.usuario_var = ctk.StringVar(self)
        self.password_var = ctk.StringVar(self)
        
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
        self.title_label = ctk.CTkLabel(self, text="👤 GESTIÓN DE PERSONAL", 
                                        font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="ew")

        self.message_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14), text_color="yellow")
        self.message_label.grid(row=1, column=0, pady=5, padx=20, sticky="ew")

        # Contenedor principal scrollable para el formulario
        scroll_frame = ctk.CTkScrollableFrame(self, fg_color="#3c3c3c", corner_radius=10, label_text="DATOS DEL EMPLEADO")
        scroll_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        scroll_frame.columnconfigure((0, 1), weight=1)
        
        # --- Sección de Búsqueda ---
        search_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        search_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="ew")
        search_frame.columnconfigure(0, weight=1)
        
        ctk.CTkLabel(search_frame, text="Buscar Personal (ID o Cédula)", font=("Arial", 14)).grid(row=0, column=0, sticky="w", padx=10, pady=(5, 5))
        
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.buscar_var, placeholder_text="ID o Cédula...", height=40)
        search_entry.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        ctk.CTkButton(search_frame, text="🔍 Buscar y Cargar", command=self._handle_buscar_personal, height=40,
                      fg_color="#3498db", hover_color="#2980b9").grid(row=1, column=1, padx=(10, 0), pady=(0, 10))

        # --- Campos del Formulario ---
        # Fila 1: Cédula y Teléfono
        self._add_field(scroll_frame, 2, 0, "Cédula (Obligatorio):", self.cedula_var)
        self._add_field(scroll_frame, 2, 1, "Teléfono:", self.telefono_var)
        
        # Fila 2: Nombres
        self._add_field(scroll_frame, 4, 0, "Primer Nombre (Obligatorio):", self.p_nombre_var)
        self._add_field(scroll_frame, 4, 1, "Segundo Nombre:", self.s_nombre_var)
        
        # Fila 3: Apellidos
        self._add_field(scroll_frame, 6, 0, "Primer Apellido (Obligatorio):", self.p_apellido_var)
        self._add_field(scroll_frame, 6, 1, "Segundo Apellido:", self.s_apellido_var)
        
        # Fila 4: Género y Cargo
        self._add_field(scroll_frame, 8, 0, "Género:", self.genero_var, is_combo="genero")
        self._add_field(scroll_frame, 8, 1, "Cargo:", self.cargo_var, is_combo="cargo")

        # Fila 5: Dirección
        self._add_field(scroll_frame, 10, 0, "Dirección:", self.direccion_var, columnspan=2)
        
        # Separador para Usuario
        ctk.CTkFrame(scroll_frame, height=2, fg_color="#555555").grid(row=12, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 10))
        ctk.CTkLabel(scroll_frame, text="DATOS DE ACCESO", font=ctk.CTkFont(size=16, weight="bold")).grid(row=13, column=0, columnspan=2, padx=10, pady=(5, 5), sticky="w")
        
        # Fila 6: Usuario y Contraseña
        self._add_field(scroll_frame, 14, 0, "Nombre de Usuario:", self.usuario_var)
        self._add_field(scroll_frame, 14, 1, "Contraseña:", self.password_var, is_password=True)
        
        # Frame de Botones
        button_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        button_frame.grid(row=16, column=0, columnspan=2, padx=10, pady=(20, 10), sticky="ew")
        
        # Botones
        ctk.CTkButton(button_frame, text="➕ Registrar Personal", command=self._handle_crear_personal, height=45, 
                      fg_color="#2ecc71", hover_color="#27ae60", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", expand=True, fill="x", padx=5)
        
        self.btn_modificar = ctk.CTkButton(button_frame, text="✏️ Modificar", command=self._handle_actualizar_personal, height=45, 
                      fg_color="#f39c12", hover_color="#e67e22", font=ctk.CTkFont(size=16, weight="bold"), state="disabled")
        self.btn_modificar.pack(side="left", expand=True, fill="x", padx=5)
        
        self.btn_eliminar = ctk.CTkButton(button_frame, text="🗑️ Eliminar", command=self._handle_eliminar_personal, height=45, 
                      fg_color="#e74c3c", hover_color="#c0392b", font=ctk.CTkFont(size=16, weight="bold"), state="disabled")
        self.btn_eliminar.pack(side="left", expand=True, fill="x", padx=5)
        
        ctk.CTkButton(button_frame, text="🧹 Limpiar", command=self.limpiar_entradas, height=45, 
                      fg_color="#95a5a6", hover_color="#7f8c8d", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", expand=True, fill="x", padx=5)

    def _add_field(self, parent, row, column, label_text, var, is_combo=None, is_password=False, columnspan=1):
        """Función auxiliar para añadir etiquetas y campos de entrada/combobox."""
        ctk.CTkLabel(parent, text=label_text, font=("Arial", 14)).grid(row=row, column=column, columnspan=columnspan, sticky="w", padx=10, pady=(10, 5))
        
        if is_combo == "genero":
            self.genero_combo = ctk.CTkComboBox(parent, variable=var, values=["Cargando..."], height=40)
            self.genero_combo.grid(row=row + 1, column=column, columnspan=columnspan, sticky="ew", padx=10, pady=(0, 5))
        elif is_combo == "cargo":
            self.cargo_combo = ctk.CTkComboBox(parent, variable=var, values=["Cargando..."], height=40)
            self.cargo_combo.grid(row=row + 1, column=column, columnspan=columnspan, sticky="ew", padx=10, pady=(0, 5))
        else:
            show_char = "*" if is_password else None
            ctk.CTkEntry(parent, textvariable=var, height=40, show=show_char).grid(row=row + 1, column=column, columnspan=columnspan, sticky="ew", padx=10, pady=(0, 5))

    # ----------------------------------------------------------------------
    # Métodos de Eventos (Delegación al Controlador)
    # ----------------------------------------------------------------------
    
    def _handle_crear_personal(self):
        data = self._obtener_datos_formulario()
        self.controller.handle_crear_personal(data)
            
    def _handle_buscar_personal(self):
        termino = self.buscar_var.get().strip()
        if not termino:
            self.display_message("❌ Ingrese ID o Cédula para buscar.", is_success=False)
            self.limpiar_entradas(clean_search=False)
        else:
            self.controller.handle_cargar_personal(termino)

            
    def _handle_actualizar_personal(self):
        if not self.personal_id_cargado:
            self.display_message("❌ Primero debe buscar y cargar un Personal para modificarlo.", is_success=False)
            return

        data = self._obtener_datos_formulario()
        data['id'] = self.personal_id_cargado
        self.controller.handle_actualizar_personal(data)
            
    def _handle_eliminar_personal(self):
        if not self.personal_id_cargado:
            self.display_message("❌ Primero debe buscar y cargar un Personal para eliminarlo.", is_success=False)
            return
            
        nombre = f"{self.p_nombre_var.get()} {self.p_apellido_var.get()}"
        if messagebox.askyesno("⚠️ Confirmación", f"¿Está seguro de que desea eliminar a {nombre} (ID: {self.personal_id_cargado})?"):
            self.controller.handle_eliminar_personal(self.personal_id_cargado)
    
    # ----------------------------------------------------------------------
    # Métodos de Mutación de Vista (Llamados por el Controlador)
    # ----------------------------------------------------------------------

    def limpiar_entradas(self, clean_search=True): 
        """Limpia todos los campos del formulario."""
        if clean_search: self.buscar_var.set("")
        self.cedula_var.set("")
        self.p_nombre_var.set("")
        self.s_nombre_var.set("")
        self.p_apellido_var.set("")
        self.s_apellido_var.set("")
        self.telefono_var.set("")
        self.direccion_var.set("")
        
        # Resetear ComboBoxes
        if self.genero_combo.cget("values"): self.genero_var.set(self.genero_combo.cget("values")[0])
        if self.cargo_combo.cget("values"): self.cargo_var.set(self.cargo_combo.cget("values")[0])
             
        self.usuario_var.set("")
        self.password_var.set("")
        self.personal_id_cargado = None
        self._set_btn_state("disabled")
        self.display_message("")

    def _obtener_datos_formulario(self): 
        """Recolecta los datos de los campos de entrada. Usa None para campos opcionales vacíos."""
        
        def _get_or_none(var):
            value = var.get().strip()
            return value if value else None

        return {
            "cedula": _get_or_none(self.cedula_var),
            "primer_nombre": _get_or_none(self.p_nombre_var),
            "segundo_nombre": _get_or_none(self.s_nombre_var),
            "primer_apellido": _get_or_none(self.p_apellido_var),
            "segundo_apellido": _get_or_none(self.s_apellido_var),
            "telefono": _get_or_none(self.telefono_var),
            "direccion": _get_or_none(self.direccion_var),
            "genero": self.genero_var.get(),
            "cargo": self.cargo_var.get(), 
            "nombre_usuario": _get_or_none(self.usuario_var),
            "password": self.password_var.get().strip() 
        }
        
    def _establecer_datos_formulario(self, data: dict): 
        """Establece los valores en los campos de entrada y habilita botones."""
        self.cedula_var.set(data.get("documento_identidad", "") or "")
        self.p_nombre_var.set(data.get("primer_nombre", "") or "")
        self.s_nombre_var.set(data.get("segundo_nombre", "") or "")
        self.p_apellido_var.set(data.get("primer_apellido", "") or "")
        self.s_apellido_var.set(data.get("segundo_apellido", "") or "")
        self.telefono_var.set(data.get("telefono", "") or "")
        self.direccion_var.set(data.get("direccion", "") or "")
        
        # Cargar Género y Cargo
        self.genero_var.set(data.get("genero", self.genero_var.cget("value")))
        self.cargo_var.set(data.get("cargo_nombre", self.cargo_var.cget("value")))

        self.usuario_var.set(data.get("nombre_usuario", "") or "")
        self.password_var.set("********") # Nunca cargar la contraseña real
        
        self.personal_id_cargado = data.get("id")
        self.buscar_var.set(str(data.get("id", "")))
        self._set_btn_state("normal")
        
    def _cargar_generos(self, generos: List[str]):
        """Carga las opciones en el ComboBox de Género."""
        if generos:
            self.genero_combo.configure(values=generos)
            self.genero_var.set(generos[0])
            
    def _cargar_cargos(self, cargos: List[str]):
        """Carga las opciones en el ComboBox de Cargo."""
        if cargos:
            self.cargo_combo.configure(values=cargos)
            self.cargo_var.set(cargos[0])
        
    def _set_btn_state(self, state):
        """Habilita o deshabilita los botones de Modificar/Eliminar."""
        self.btn_modificar.configure(state=state)
        self.btn_eliminar.configure(state=state)
        
    def display_message(self, message: str, is_success: bool = True):
        """Muestra un mensaje de estado en la interfaz."""
        color = "#2ecc71" if is_success else "#e74c3c"
        self.message_label.configure(text=message, text_color=color)