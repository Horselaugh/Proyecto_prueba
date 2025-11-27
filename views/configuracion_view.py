import customtkinter as ctk 
from tkinter import messagebox
from typing import List, Dict, Any, Optional
from controllers.configuracion_controller import ConfiguracionControlador

class ConfiguracionViewFrame(ctk.CTkFrame):
    
    def __init__(self, master, controller: ConfiguracionControlador):
        super().__init__(master, corner_radius=0, fg_color="transparent") 
        
        self.controller = controller 
        self.controller.set_view(self) 
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1) 
        
        # --- Variables de Estado de Roles ---
        self.rol_id_var: Optional[int] = None
        self.rol_nombre_var = ctk.StringVar(self, value="")
        self.rol_desc_var = ctk.StringVar(self, value="")
        
        # --- Variables de Estado de Usuarios ---
        self.usuario_id_var: Optional[int] = None
        self.usuario_doc_var = ctk.StringVar(self, value="")
        self.usuario_nombre_var = ctk.StringVar(self, value="")
        self.usuario_apellido_var = ctk.StringVar(self, value="")
        self.usuario_rol_var = ctk.StringVar(self, value="Seleccionar Rol")
        
        # --- Widgets (Inicializados a None para W0201) ---
        self.rol_list_frame: Optional[ctk.CTkScrollableFrame] = None
        self.rol_form_frame: Optional[ctk.CTkFrame] = None
        self.btn_rol_crear_guardar: Optional[ctk.CTkButton] = None
        self.btn_rol_cancelar: Optional[ctk.CTkButton] = None
        self.btn_rol_eliminar: Optional[ctk.CTkButton] = None
        self.rol_map: Dict[int, str] = {} # Mapeo de ID a Nombre/Desc para uso interno

        self.usuario_list_frame: Optional[ctk.CTkScrollableFrame] = None
        self.usuario_form_frame: Optional[ctk.CTkFrame] = None
        self.usuario_rol_combo: Optional[ctk.CTkComboBox] = None
        self.usuario_doc_entry: Optional[ctk.CTkEntry] = None
        self.btn_usuario_crear_guardar: Optional[ctk.CTkButton] = None
        self.btn_usuario_cancelar: Optional[ctk.CTkButton] = None
        self.btn_usuario_eliminar: Optional[ctk.CTkButton] = None
        
        self._configurar_interfaz()

    def show(self):
        """Llamado por MenuApp, invoca la carga de datos iniciales del controlador."""
        self.controller.load_initial_data() 

    def _configurar_interfaz(self):
        """Configura la interfaz gráfica."""
        
        # Título y Mensaje
        self.title_label = ctk.CTkLabel(self, text="⚙️ CONFIGURACIÓN", 
                                        font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="ew")

        self.message_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14), 
                                          text_color="yellow")
        self.message_label.grid(row=0, column=0, pady=(60, 0), padx=20, sticky="n")

        # Frame principal con las dos pestañas (Roles y Usuarios)
        main_tabview = ctk.CTkTabview(self, fg_color="transparent")
        main_tabview.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        main_tabview.add("👤 Roles")
        main_tabview.add("👥 Usuarios")
        
        # Configurar las pestañas
        self._configurar_tab_roles(main_tabview.tab("👤 Roles"))
        self._configurar_tab_usuarios(main_tabview.tab("👥 Usuarios"))

    # ======================================================================
    # PESTAÑA DE ROLES
    # ======================================================================

    def _configurar_tab_roles(self, tab_frame: ctk.CTkFrame):
        """Configura la interfaz de la pestaña de Roles."""
        tab_frame.columnconfigure(0, weight=1)
        tab_frame.columnconfigure(1, weight=1)
        tab_frame.rowconfigure(0, weight=1)

        # 1. Lista de Roles Existentes
        self.rol_list_frame = ctk.CTkScrollableFrame(tab_frame, 
                                                     label_text="Roles Existentes", 
                                                     fg_color="#2e2e2e")
        self.rol_list_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.rol_list_frame.columnconfigure(0, weight=1)

        # 2. Formulario de Creación/Edición de Roles
        self.rol_form_frame = ctk.CTkFrame(tab_frame, fg_color="#111111", 
                                           corner_radius=10)
        self.rol_form_frame.grid(row=0, column=1, sticky="nwe", padx=10, pady=10)
        self.rol_form_frame.columnconfigure(0, weight=1)

        ctk.CTkLabel(self.rol_form_frame, text="Gestión de Roles", 
                     font=ctk.CTkFont(size=18, weight="bold")).pack(pady=15)

        # Nombre del Rol
        ctk.CTkLabel(self.rol_form_frame, text="Nombre del Rol:").pack(padx=20, 
                                                                      pady=(5, 0), 
                                                                      fill="x")
        ctk.CTkEntry(self.rol_form_frame, textvariable=self.rol_nombre_var).pack(padx=20, 
                                                                                pady=(0, 10), 
                                                                                fill="x")

        # Descripción
        ctk.CTkLabel(self.rol_form_frame, text="Descripción:").pack(padx=20, 
                                                                    pady=(5, 0), 
                                                                    fill="x")
        ctk.CTkEntry(self.rol_form_frame, textvariable=self.rol_desc_var).pack(padx=20, 
                                                                              pady=(0, 20), 
                                                                              fill="x")

        # Botones de Acción
        btn_frame = ctk.CTkFrame(self.rol_form_frame, fg_color="transparent")
        btn_frame.pack(padx=20, pady=(10, 20), fill="x")
        btn_frame.columnconfigure((0, 1), weight=1)
        
        self.btn_rol_crear_guardar = ctk.CTkButton(btn_frame, text="➕ Crear Rol", 
                                                     command=self._handle_rol_save, 
                                                     fg_color="#2ecc71", 
                                                     hover_color="#27ae60", 
                                                     height=35)
        self.btn_rol_crear_guardar.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        self.btn_rol_cancelar = ctk.CTkButton(btn_frame, text="❌ Cancelar/Nuevo", 
                                                 command=lambda: self._limpiar_campos_rol(clear_selection=True), 
                                                 fg_color="#e74c3c", 
                                                 hover_color="#c0392b", 
                                                 height=35)
        self.btn_rol_cancelar.grid(row=0, column=1, padx=(5, 0), sticky="ew")

        self.btn_rol_eliminar = ctk.CTkButton(self.rol_form_frame, 
                                                 text="🗑️ Eliminar Rol Seleccionado", 
                                                 command=self._handle_rol_eliminar, 
                                                 fg_color="#c0392b", 
                                                 hover_color="#a0291a", 
                                                 height=35, state="disabled")
        self.btn_rol_eliminar.pack(padx=20, pady=(10, 20), fill="x")


    def _cargar_roles(self, roles: List[Dict[str, Any]]):
        """
        [MÉTODO REQUERIDO POR EL CONTROLADOR] 
        Carga los roles en el marco de lista y prepara las opciones de ComboBox.
        """
        
        # Limpiar lista de roles
        for widget in self.rol_list_frame.winfo_children():
            widget.destroy()
            
        # Preparar opciones para ComboBox de Usuarios
        rol_options = ["Seleccionar Rol"]
        # Mapeo de ID a Nombre/Desc para uso interno. Inicializado en __init__.
        self.rol_map = {} 
        
        # Guardar la selección actual del ComboBox de usuarios
        current_user_rol_selection = self.usuario_rol_var.get()
        
        for rol in roles:
            # Asegurar que se usan los nombres correctos de las claves del diccionario
            rol_str = f"{rol['id']} - {rol['nombre']}"
            rol_options.append(rol_str)
            self.rol_map[rol['id']] = rol_str

            # Crear elemento en la lista (visualización)
            rol_frame = ctk.CTkFrame(self.rol_list_frame, fg_color="#34495e", 
                                     corner_radius=8)
            rol_frame.pack(fill="x", padx=10, pady=(6, 3))
            
            ctk.CTkLabel(rol_frame, text=rol_str, 
                         font=ctk.CTkFont(size=14, weight="bold"), 
                         anchor="w").pack(padx=10, pady=(5, 0), fill="x")
            ctk.CTkLabel(rol_frame, text=rol['descripcion'], anchor="w", 
                         wraplength=400).pack(padx=10, pady=(0, 5), fill="x")

            btn_edit = ctk.CTkButton(rol_frame, text="Editar", width=60, 
                                     command=lambda r=rol: self._cargar_rol_para_edicion(r))
            btn_edit.pack(side="right", padx=10, pady=5)
            
        # Actualizar ComboBox de Usuarios si existe
        if self.usuario_rol_combo:
            self.usuario_rol_combo.configure(values=rol_options)
            # Intentar mantener la selección si sigue existiendo. Si no, poner el default.
            if current_user_rol_selection in rol_options:
                self.usuario_rol_var.set(current_user_rol_selection)
            elif rol_options: 
                # Solo si hay roles, establece el primero o el default
                if len(rol_options) > 0:
                    self.usuario_rol_var.set(rol_options[0])
                else:
                    self.usuario_rol_var.set("Seleccionar Rol")


    def _cargar_rol_para_edicion(self, rol_data: Dict[str, Any]):
        """Carga los datos de un rol en el formulario para edición."""
        self.rol_id_var = rol_data['id']
        self.rol_nombre_var.set(rol_data['nombre'])
        self.rol_desc_var.set(rol_data['descripcion'])
        self.btn_rol_crear_guardar.configure(text="💾 Guardar Cambios", 
                                             fg_color="#3498db", 
                                             hover_color="#2980b9")
        self.btn_rol_eliminar.configure(state="normal")
        self.display_message(f"Cargado Rol ID {rol_data['id']} para edición.", True)

    def _limpiar_campos_rol(self, clear_selection: bool = False):
        """
        [MÉTODO REQUERIDO POR EL CONTROLADOR]
        Limpia los campos del formulario de Roles.
        """
        if clear_selection:
            self.rol_id_var = None
        self.rol_nombre_var.set("")
        self.rol_desc_var.set("")
        self.btn_rol_crear_guardar.configure(text="➕ Crear Rol", 
                                             fg_color="#2ecc71", 
                                             hover_color="#27ae60")
        self.btn_rol_eliminar.configure(state="disabled")
        self.display_message("Formulario de Rol listo para un nuevo registro.", True)


    # --- Handlers de Rol ---
    
    def _handle_rol_save(self):
        """Maneja la creación o edición de un rol."""
        data = {
            'id': self.rol_id_var, # Será None si es creación
            'nombre': self.rol_nombre_var.get().strip(),
            'descripcion': self.rol_desc_var.get().strip()
        }

        if data['id'] is None:
            self.controller.handle_crear_rol(data)
        else:
            self.controller.handle_guardar_rol(data)

    def _handle_rol_eliminar(self):
        """Maneja la eliminación de un rol."""
        if self.rol_id_var is not None:
            nombre = self.rol_nombre_var.get()
            # En una aplicación real, usaríamos un modal para confirmar
            if messagebox.askyesno("Confirmar Eliminación", 
                                   f"¿Está seguro de eliminar el rol '{nombre}' (ID: {self.rol_id_var})?"):
                self.controller.handle_eliminar_rol(self.rol_id_var, nombre)
        else:
            self.display_message("❌ Seleccione un rol para eliminar.", 
                                 is_success=False)


    # ======================================================================
    # PESTAÑA DE USUARIOS
    # ======================================================================

    def _configurar_tab_usuarios(self, tab_frame: ctk.CTkFrame):
        """Configura la interfaz de la pestaña de Usuarios."""
        tab_frame.columnconfigure(0, weight=1)
        tab_frame.columnconfigure(1, weight=1)
        tab_frame.rowconfigure(0, weight=1)

        # 1. Lista de Usuarios Existentes
        self.usuario_list_frame = ctk.CTkScrollableFrame(tab_frame, 
                                                         label_text="Usuarios Existentes", 
                                                         fg_color="#2e2e2e")
        self.usuario_list_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.usuario_list_frame.columnconfigure(0, weight=1)

        # 2. Formulario de Creación/Edición de Usuarios
        self.usuario_form_frame = ctk.CTkFrame(tab_frame, fg_color="#111111", 
                                               corner_radius=10)
        self.usuario_form_frame.grid(row=0, column=1, sticky="nwe", padx=10, pady=10)
        self.usuario_form_frame.columnconfigure(0, weight=1)

        ctk.CTkLabel(self.usuario_form_frame, text="Gestión de Usuarios", 
                     font=ctk.CTkFont(size=18, weight="bold")).pack(pady=15)

        # Documento
        ctk.CTkLabel(self.usuario_form_frame, text="Documento (ID único):").pack(padx=20, 
                                                                                 pady=(5, 0), 
                                                                                 fill="x")
        self.usuario_doc_entry = ctk.CTkEntry(self.usuario_form_frame, 
                                              textvariable=self.usuario_doc_var)
        self.usuario_doc_entry.pack(padx=20, pady=(0, 10), fill="x")

        # Nombre
        ctk.CTkLabel(self.usuario_form_frame, text="Primer Nombre:").pack(padx=20, 
                                                                          pady=(5, 0), 
                                                                          fill="x")
        ctk.CTkEntry(self.usuario_form_frame, textvariable=self.usuario_nombre_var).pack(padx=20, 
                                                                                        pady=(0, 10), 
                                                                                        fill="x")
        
        # Apellido
        ctk.CTkLabel(self.usuario_form_frame, text="Apellido:").pack(padx=20, 
                                                                     pady=(5, 0), 
                                                                     fill="x")
        ctk.CTkEntry(self.usuario_form_frame, textvariable=self.usuario_apellido_var).pack(padx=20, 
                                                                                          pady=(0, 10), 
                                                                                          fill="x")

        # Rol
        ctk.CTkLabel(self.usuario_form_frame, text="Rol Asignado:").pack(padx=20, 
                                                                         pady=(5, 0), 
                                                                         fill="x")
        self.usuario_rol_combo = ctk.CTkComboBox(self.usuario_form_frame, 
                                                 variable=self.usuario_rol_var, 
                                                 values=["Seleccionar Rol"], # Se actualiza
                                                 height=35)
        self.usuario_rol_combo.pack(padx=20, pady=(0, 20), fill="x")

        # Botones de Acción
        btn_frame_user = ctk.CTkFrame(self.usuario_form_frame, fg_color="transparent")
        btn_frame_user.pack(padx=20, pady=(10, 20), fill="x")
        btn_frame_user.columnconfigure((0, 1), weight=1)
        
        self.btn_usuario_crear_guardar = ctk.CTkButton(btn_frame_user, 
                                                         text="➕ Crear Usuario", 
                                                         command=self._handle_usuario_save, 
                                                         fg_color="#2ecc71", 
                                                         hover_color="#27ae60", 
                                                         height=35)
        self.btn_usuario_crear_guardar.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        self.btn_usuario_cancelar = ctk.CTkButton(btn_frame_user, 
                                                     text="❌ Cancelar/Nuevo", 
                                                     command=lambda: self._limpiar_campos_usuario(clear_selection=True), 
                                                     fg_color="#e74c3c", 
                                                     hover_color="#c0392b", 
                                                     height=35)
        self.btn_usuario_cancelar.grid(row=0, column=1, padx=(5, 0), sticky="ew")

        self.btn_usuario_eliminar = ctk.CTkButton(self.usuario_form_frame, 
                                                     text="🗑️ Eliminar Usuario Seleccionado", 
                                                     command=self._handle_usuario_eliminar, 
                                                     fg_color="#c0392b", 
                                                     hover_color="#a0291a", 
                                                     height=35, state="disabled")
        self.btn_usuario_eliminar.pack(padx=20, pady=(10, 20), fill="x")


    def _cargar_usuarios(self, usuarios: List[Dict[str, Any]]):
        """
        [MÉTODO REQUERIDO POR EL CONTROLADOR]
        Carga los usuarios en el marco de lista.
        """
        
        # Limpiar lista de usuarios
        for widget in self.usuario_list_frame.winfo_children():
            widget.destroy()
            
        for usuario in usuarios:
            # Crear elemento en la lista (visualización)
            user_frame = ctk.CTkFrame(self.usuario_list_frame, fg_color="#34495e", 
                                     corner_radius=8)
            user_frame.pack(fill="x", padx=10, pady=(6, 3))
            
            # Nota: El controlador trae 'nombre_usuario' (que es primer_nombre) y 'primer_apellido'
            # del modelo real.
            nombre_completo = f"{usuario['nombre_usuario']} {usuario['primer_apellido']} ({usuario['rol_nombre']})"
            
            ctk.CTkLabel(user_frame, 
                         text=nombre_completo, 
                         font=ctk.CTkFont(size=14, weight="bold"), 
                         anchor="w").pack(padx=10, pady=(5, 0), fill="x")
            
            ctk.CTkLabel(user_frame, 
                         text=f"Doc: {usuario['documento_identidad']} | ID: {usuario['persona_id']}", 
                         anchor="w", text_color="#bdc3c7").pack(padx=10, pady=(0, 5), fill="x")

            btn_edit = ctk.CTkButton(user_frame, text="Editar", width=60, 
                                     # Se ajustan las claves para coincidir con lo que trae el modelo
                                     command=lambda u=usuario: self._cargar_usuario_para_edicion({
                                         'id': u['persona_id'], # El ID de la persona
                                         'documento': u['documento_identidad'],
                                         'primer_nombre': u['nombre_usuario'], # Es el primer_nombre
                                         'apellido': u['primer_apellido'],
                                         'rol_id': u['rol_id'],
                                         'rol_nombre': u['rol_nombre']
                                     }))
            btn_edit.pack(side="right", padx=10, pady=5)


    def _cargar_usuario_para_edicion(self, usuario_data: Dict[str, Any]):
        """Carga los datos de un usuario en el formulario para edición."""
        self.usuario_id_var = usuario_data['id']
        
        # El documento se debe deshabilitar en edición si se usa como ID único
        self.usuario_doc_var.set(usuario_data['documento'])
        self.usuario_doc_entry.configure(state="disabled") 
        
        self.usuario_nombre_var.set(usuario_data['primer_nombre'])
        self.usuario_apellido_var.set(usuario_data['apellido'])
        
        # Seleccionar el rol correcto en el ComboBox
        rol_id = usuario_data.get('rol_id')
        rol_nombre = usuario_data.get('rol_nombre', 'N/A')
        
        # La opción en el ComboBox está en el formato 'ID - Nombre'
        opcion_a_seleccionar = f"{rol_id} - {rol_nombre}"
        
        combo_values = self.usuario_rol_combo.cget("values")
        if opcion_a_seleccionar in combo_values:
            self.usuario_rol_var.set(opcion_a_seleccionar)
        else:
            # Se usa el primer valor de la lista si el rol actual ya no existe
            default_value = combo_values[0] if combo_values else "Seleccionar Rol"
            self.usuario_rol_var.set(default_value)

        self.btn_usuario_crear_guardar.configure(text="💾 Guardar Cambios", 
                                                 fg_color="#3498db", 
                                                 hover_color="#2980b9")
        self.btn_usuario_eliminar.configure(state="normal")
        self.display_message(f"Cargado Usuario ID {usuario_data['id']} para edición.", 
                             True)

    def _limpiar_campos_usuario(self, clear_selection: bool = False):
        """
        [MÉTODO REQUERIDO POR EL CONTROLADOR]
        Limpia los campos del formulario de Usuarios.
        """
        if clear_selection:
            self.usuario_id_var = None
        self.usuario_doc_var.set("")
        if self.usuario_doc_entry: # Comprobación de seguridad
            # Habilitar Documento para nuevo registro
            self.usuario_doc_entry.configure(state="normal") 
        self.usuario_nombre_var.set("")
        self.usuario_apellido_var.set("")
        
        # Resetear el ComboBox al valor por defecto
        combo_values = self.usuario_rol_combo.cget("values") if self.usuario_rol_combo else []
        default_value = combo_values[0] if combo_values else "Seleccionar Rol"
        self.usuario_rol_var.set(default_value)
        
        self.btn_usuario_crear_guardar.configure(text="➕ Crear Usuario", 
                                                 fg_color="#2ecc71", 
                                                 hover_color="#27ae60")
        self.btn_usuario_eliminar.configure(state="disabled")
        self.display_message("Formulario de Usuario listo para un nuevo registro.", True)


    # --- Handlers de Usuario ---
    
    def _handle_usuario_save(self):
        """Maneja la creación o edición de un usuario."""
        rol_str = self.usuario_rol_var.get()
        # Obtener el rol_id de la cadena, usando el método del controlador real
        rol_id = self.controller.get_rol_id_from_str(rol_str) 
        
        data = {
            'id': self.usuario_id_var, # Será None si es creación
            'documento': self.usuario_doc_var.get().strip(),
            'primer_nombre': self.usuario_nombre_var.get().strip(),
            'apellido': self.usuario_apellido_var.get().strip(),
            'rol_id': rol_id,
            'rol_str': rol_str # Necesario para _prepare_usuario_data en el controlador
        }

        if data['id'] is None:
            self.controller.handle_crear_usuario(data)
        else:
            self.controller.handle_guardar_usuario(data)

    def _handle_usuario_eliminar(self):
        """Maneja la eliminación de un usuario."""
        if self.usuario_id_var is not None:
            nombre = f"{self.usuario_nombre_var.get()} {self.usuario_apellido_var.get()}"
            # En una aplicación real, usaríamos un modal para confirmar
            if messagebox.askyesno("Confirmar Eliminación", 
                                   f"¿Está seguro de eliminar al usuario '{nombre}' (ID: {self.usuario_id_var})?"):
                self.controller.handle_eliminar_usuario(self.usuario_id_var, nombre)
        else:
            self.display_message("❌ Seleccione un usuario para eliminar.", 
                                 is_success=False)


    # ======================================================================
    # MÉTODO DE UTILIDAD
    # ======================================================================

    def display_message(self, message: str, is_success: bool = True):
        """Muestra un mensaje de estado en la interfaz."""
        color = "#2ecc71" if is_success else "#e74c3c"
        self.message_label.configure(text=message, text_color=color)