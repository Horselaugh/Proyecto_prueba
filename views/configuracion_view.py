import customtkinter as ctk
from tkinter import messagebox
from typing import List, Dict, Any, Optional
import random

# ----------------------------------------------------------------------
# MOCK DE MODELO (TEMPORAL) - COMPLETO Y REVISADO
# ----------------------------------------------------------------------

# MOCK TEMPORAL: Asegura que el Controlador pueda inicializar su propiedad 'modelo'
# e incluye todos los métodos CRUD necesarios para evitar AttributeErrors.
class MockConfiguracionModelo:
    """Mock completo del Modelo de configuración para simular la persistencia de datos."""
    
    # Simulación de datos en memoria para el mock
    _ROLES = [
        {"id": 1, "nombre": "Admin", "descripcion": "Administrador con control total"},
        {"id": 2, "nombre": "Supervisor", "descripcion": "Puede aprobar y auditar"},
        {"id": 3, "nombre": "Usuario", "descripcion": "Acceso básico para registro"}
    ]
    _USUARIOS = [
        {"id": 101, "primer_nombre": "Juan", "apellido": "Perez", "documento": "12345678", "rol_id": 1, "rol_nombre": "Admin"},
        {"id": 102, "primer_nombre": "Maria", "apellido": "Lopez", "documento": "87654321", "rol_id": 3, "rol_nombre": "Usuario"},
    ]
    
    # ------------------
    # ROLES
    # ------------------
    def get_all_roles(self) -> List[Dict[str, Any]]: 
        """Retorna una lista simulada de roles."""
        return self._ROLES

    def handle_crear_rol(self, data: Dict[str, str]) -> bool: 
        """Mock para crear un nuevo rol."""
        new_id = max([r['id'] for r in self._ROLES], default=0) + 1
        new_rol = {"id": new_id, "nombre": data['nombre'], "descripcion": data['descripcion']}
        self._ROLES.append(new_rol)
        return True

    def handle_guardar_rol(self, data: Dict[str, Any]) -> bool: 
        """Mock para actualizar un rol existente."""
        for i, rol in enumerate(self._ROLES):
            if rol['id'] == data['id']:
                self._ROLES[i]['nombre'] = data['nombre']
                self._ROLES[i]['descripcion'] = data['descripcion']
                return True
        return False
        
    def handle_eliminar_rol(self, rol_id: int) -> bool: 
        """Mock para eliminar un rol."""
        # Se recrea la lista excluyendo el rol_id
        self._ROLES[:] = [r for r in self._ROLES if r['id'] != rol_id]
        
        # También actualizamos los usuarios cuyo rol fue eliminado, asignándoles el primer rol disponible o un default.
        # En una aplicación real, habría validación para prevenir esto.
        if not self._ROLES:
            default_rol_id = None
        else:
            default_rol_id = self._ROLES[0]['id']
            default_rol_nombre = self._ROLES[0]['nombre']
            
        for user in self._USUARIOS:
            if user['rol_id'] == rol_id:
                user['rol_id'] = default_rol_id
                user['rol_nombre'] = default_rol_nombre if default_rol_id else "N/A (Rol Eliminado)"
                
        return True

    # ------------------
    # USUARIOS
    # ------------------
    def get_all_usuarios(self) -> List[Dict[str, Any]]: 
        """Retorna una lista simulada de usuarios."""
        return self._USUARIOS
        
    def handle_crear_usuario(self, data: Dict[str, Any]) -> bool: 
        """Mock para crear un nuevo usuario."""
        new_id = max([u['id'] for u in self._USUARIOS], default=100) + 1
        rol_info = self._get_rol_info(data['rol_id'])
        new_user = {
            "id": new_id, 
            "primer_nombre": data['primer_nombre'], 
            "apellido": data['apellido'], 
            "documento": data['documento'], 
            "rol_id": data['rol_id'],
            "rol_nombre": rol_info.get('nombre', 'Desconocido')
        }
        self._USUARIOS.append(new_user)
        return True
        
    def handle_guardar_usuario(self, data: Dict[str, Any]) -> bool: 
        """Mock para actualizar un usuario existente."""
        for i, user in enumerate(self._USUARIOS):
            if user['id'] == data['id']:
                rol_info = self._get_rol_info(data['rol_id'])
                self._USUARIOS[i].update({
                    "primer_nombre": data['primer_nombre'],
                    "apellido": data['apellido'],
                    "documento": data['documento'],
                    "rol_id": data['rol_id'],
                    "rol_nombre": rol_info.get('nombre', 'Desconocido')
                })
                return True
        return False

    def handle_eliminar_usuario(self, persona_id: int) -> bool: 
        """Mock para eliminar un usuario."""
        self._USUARIOS[:] = [u for u in self._USUARIOS if u['id'] != persona_id]
        return True
        
    def _get_rol_info(self, rol_id: int) -> Dict[str, Any]:
        """Ayudante para obtener nombre de rol en el mock."""
        for rol in self._ROLES:
            if rol['id'] == rol_id:
                return rol
        # Retorna un diccionario con valores por defecto si el rol_id no se encuentra
        return {"id": None, "nombre": "Desconocido", "descripcion": "Rol no encontrado"}


# Importamos el controlador (o su mock)
try:
    # Esto asume que tienes un controlador real, si no, usa el mock
    from controllers.configuracion_controller import ConfiguracionControlador
except ImportError:
    # MOCK del Controlador si la importación real falla
    class MockConfiguracionControlador:
        """Controlador simple para probar la vista sin backend."""
        def __init__(self):
            # Usar el mock de modelo completo para evitar errores de Attribute
            self.modelo = MockConfiguracionModelo()
            self.vista: Optional['ConfiguracionViewFrame'] = None

        def set_view(self, view_instance):
            self.vista = view_instance

        def get_rol_id_from_str(self, rol_str: str) -> Optional[int]:
            """Extrae el ID numérico del rol desde la cadena (e.g., '1 - Admin')"""
            try:
                if rol_str and ' - ' in rol_str:
                    return int(rol_str.split(' - ')[0])
            except ValueError:
                return None
            return None

        def get_all_roles(self):
            return self.modelo.get_all_roles()

        def load_initial_data(self):
            """Carga los datos iniciales (roles y usuarios) en la vista."""
            if self.vista:
                roles = self.get_all_roles()
                usuarios = self.modelo.get_all_usuarios()
                self.vista._cargar_roles(roles)
                self.vista._cargar_usuarios(usuarios)
                self.vista.display_message("✅ Datos de Configuración cargados (Mock).", is_success=True)

        def _validar_rol_data(self, data: Dict[str, str]) -> bool:
            if not data.get('nombre') or not data.get('descripcion'):
                self.vista.display_message("❌ Error: Nombre y descripción del rol son obligatorios.", is_success=False)
                return False
            return True

        def handle_crear_rol(self, data: Dict[str, str]):
            if not self._validar_rol_data(data): return
            if self.modelo.handle_crear_rol(data):
                self.vista.display_message(f"✅ Rol {data['nombre']} creado.", is_success=True)
                self.vista._limpiar_campos_rol(clear_selection=True)
                self.load_initial_data()
            else:
                self.vista.display_message(f"❌ Error al crear rol.", is_success=False)

        def handle_guardar_rol(self, data: Dict[str, Any]):
            if not self._validar_rol_data(data): return
            if self.modelo.handle_guardar_rol(data):
                self.vista.display_message(f"✅ Rol {data['nombre']} guardado.", is_success=True)
                self.vista._limpiar_campos_rol(clear_selection=True)
                self.load_initial_data()
            else:
                self.vista.display_message(f"❌ Error al guardar rol.", is_success=False)

        def handle_eliminar_rol(self, rol_id: int, nombre_rol: str):
            if self.modelo.handle_eliminar_rol(rol_id):
                self.vista.display_message(f"🗑️ Rol {nombre_rol} eliminado.", is_success=True)
                self.vista._limpiar_campos_rol(clear_selection=True)
                self.load_initial_data()
            else:
                self.vista.display_message(f"❌ Error al eliminar rol.", is_success=False)
        
        # --- USUARIOS ---

        def _validar_usuario_data(self, data: Dict[str, Any]) -> bool:
            if not data.get('primer_nombre') or not data.get('documento'):
                self.vista.display_message("❌ Error: Nombre y documento son obligatorios.", is_success=False)
                return False
            if not data.get('rol_id'):
                self.vista.display_message("❌ Error: Debe seleccionar un Rol para el usuario.", is_success=False)
                return False
            return True

        def handle_crear_usuario(self, data: Dict[str, Any]):
            if not self._validar_usuario_data(data): return
            if self.modelo.handle_crear_usuario(data):
                self.vista.display_message(f"✅ Usuario {data['primer_nombre']} creado.", is_success=True)
                self.vista._limpiar_campos_usuario(clear_selection=True)
                self.load_initial_data()
            else:
                self.vista.display_message(f"❌ Error al crear usuario.", is_success=False)

        def handle_guardar_usuario(self, data: Dict[str, Any]):
            if not self._validar_usuario_data(data): return
            if self.modelo.handle_guardar_usuario(data):
                self.vista.display_message(f"✅ Usuario {data['primer_nombre']} guardado.", is_success=True)
                self.vista._limpiar_campos_usuario(clear_selection=True)
                self.load_initial_data()
            else:
                self.vista.display_message(f"❌ Error al guardar usuario.", is_success=False)

        def handle_eliminar_usuario(self, persona_id: int, nombre_usuario: str):
            if self.modelo.handle_eliminar_usuario(persona_id):
                self.vista.display_message(f"🗑️ Usuario {nombre_usuario} eliminado.", is_success=True)
                self.vista._limpiar_campos_usuario(clear_selection=True)
                self.load_initial_data()
            else:
                self.vista.display_message(f"❌ Error al eliminar usuario.", is_success=False)

    ConfiguracionControlador = MockConfiguracionControlador


class ConfiguracionViewFrame(ctk.CTkFrame):
    """
    Vista para el módulo de configuración. 
    Hereda de CTkFrame para ser cargado en el panel de contenido.
    """
    
    def __init__(self, master, controller: MockConfiguracionControlador):
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
        
        # --- Widgets ---
        self.rol_list_frame: Optional[ctk.CTkScrollableFrame] = None
        self.usuario_list_frame: Optional[ctk.CTkScrollableFrame] = None
        self.usuario_rol_combo: Optional[ctk.CTkComboBox] = None
        self.usuario_doc_entry: Optional[ctk.CTkEntry] = None

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

        self.message_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14), text_color="yellow")
        self.message_label.grid(row=0, column=0, pady=(60, 0), padx=20, sticky="n") # Ubicación fija

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
        tab_frame.columnconfigure(0, weight=1)
        tab_frame.columnconfigure(1, weight=1)
        tab_frame.rowconfigure(0, weight=1)

        # 1. Lista de Roles Existentes
        self.rol_list_frame = ctk.CTkScrollableFrame(tab_frame, label_text="Roles Existentes", fg_color="#2e2e2e")
        self.rol_list_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.rol_list_frame.columnconfigure(0, weight=1)

        # 2. Formulario de Creación/Edición de Roles
        self.rol_form_frame = ctk.CTkFrame(tab_frame, fg_color="#111111", corner_radius=10)
        self.rol_form_frame.grid(row=0, column=1, sticky="nwe", padx=10, pady=10)
        self.rol_form_frame.columnconfigure(0, weight=1)

        ctk.CTkLabel(self.rol_form_frame, text="Gestión de Roles", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=15)

        # Nombre del Rol
        ctk.CTkLabel(self.rol_form_frame, text="Nombre del Rol:").pack(padx=20, pady=(5, 0), fill="x")
        ctk.CTkEntry(self.rol_form_frame, textvariable=self.rol_nombre_var).pack(padx=20, pady=(0, 10), fill="x")

        # Descripción
        ctk.CTkLabel(self.rol_form_frame, text="Descripción:").pack(padx=20, pady=(5, 0), fill="x")
        ctk.CTkEntry(self.rol_form_frame, textvariable=self.rol_desc_var).pack(padx=20, pady=(0, 20), fill="x")

        # Botones de Acción
        btn_frame = ctk.CTkFrame(self.rol_form_frame, fg_color="transparent")
        btn_frame.pack(padx=20, pady=(10, 20), fill="x")
        btn_frame.columnconfigure((0, 1), weight=1)
        
        self.btn_rol_crear_guardar = ctk.CTkButton(btn_frame, text="➕ Crear Rol", command=self._handle_rol_save, 
                                                     fg_color="#2ecc71", hover_color="#27ae60", height=35)
        self.btn_rol_crear_guardar.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        self.btn_rol_cancelar = ctk.CTkButton(btn_frame, text="❌ Cancelar/Nuevo", command=lambda: self._limpiar_campos_rol(clear_selection=True), 
                                                 fg_color="#e74c3c", hover_color="#c0392b", height=35)
        self.btn_rol_cancelar.grid(row=0, column=1, padx=(5, 0), sticky="ew")

        self.btn_rol_eliminar = ctk.CTkButton(self.rol_form_frame, text="🗑️ Eliminar Rol Seleccionado", command=self._handle_rol_eliminar, 
                                                 fg_color="#c0392b", hover_color="#a0291a", height=35, state="disabled")
        self.btn_rol_eliminar.pack(padx=20, pady=(10, 20), fill="x")


    def _cargar_roles(self, roles: List[Dict[str, Any]]):
        """Carga los roles en el marco de lista y prepara las opciones de ComboBox."""
        
        # Limpiar lista de roles
        for widget in self.rol_list_frame.winfo_children():
            widget.destroy()
            
        # Preparar opciones para ComboBox de Usuarios
        rol_options = ["Seleccionar Rol"]
        self.rol_map: Dict[int, str] = {} # Mapeo de ID a Nombre/Desc para uso interno
        
        # Guardar la selección actual del ComboBox de usuarios
        current_user_rol_selection = self.usuario_rol_var.get()
        
        for rol in roles:
            rol_str = f"{rol['id']} - {rol['nombre']}"
            rol_options.append(rol_str)
            self.rol_map[rol['id']] = rol_str

            # Crear elemento en la lista (visualización)
            rol_frame = ctk.CTkFrame(self.rol_list_frame, fg_color="#34495e", corner_radius=8)
            rol_frame.pack(fill="x", padx=10, pady=(6, 3))
            
            ctk.CTkLabel(rol_frame, text=rol_str, font=ctk.CTkFont(size=14, weight="bold"), anchor="w").pack(padx=10, pady=(5, 0), fill="x")
            ctk.CTkLabel(rol_frame, text=rol['descripcion'], anchor="w", wraplength=400).pack(padx=10, pady=(0, 5), fill="x")

            btn_edit = ctk.CTkButton(rol_frame, text="Editar", width=60, 
                                     command=lambda r=rol: self._cargar_rol_para_edicion(r))
            btn_edit.pack(side="right", padx=10, pady=5)
            
        # Actualizar ComboBox de Usuarios si existe
        if self.usuario_rol_combo:
            self.usuario_rol_combo.configure(values=rol_options)
            # Intentar mantener la selección si sigue existiendo. Si no, poner el default.
            if current_user_rol_selection in rol_options:
                self.usuario_rol_var.set(current_user_rol_selection)
            elif rol_options: # Si hay al menos una opción (el default "Seleccionar Rol")
                self.usuario_rol_var.set(rol_options[0])


    def _cargar_rol_para_edicion(self, rol_data: Dict[str, Any]):
        """Carga los datos de un rol en el formulario para edición."""
        self.rol_id_var = rol_data['id']
        self.rol_nombre_var.set(rol_data['nombre'])
        self.rol_desc_var.set(rol_data['descripcion'])
        self.btn_rol_crear_guardar.configure(text="💾 Guardar Cambios", fg_color="#3498db", hover_color="#2980b9")
        self.btn_rol_eliminar.configure(state="normal")
        self.display_message(f"Cargado Rol ID {rol_data['id']} para edición.", True)

    def _limpiar_campos_rol(self, clear_selection: bool = False):
        """Limpia los campos del formulario de Roles."""
        if clear_selection:
            self.rol_id_var = None
        self.rol_nombre_var.set("")
        self.rol_desc_var.set("")
        self.btn_rol_crear_guardar.configure(text="➕ Crear Rol", fg_color="#2ecc71", hover_color="#27ae60")
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
            if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar el rol '{nombre}' (ID: {self.rol_id_var})?"):
                self.controller.handle_eliminar_rol(self.rol_id_var, nombre)
        else:
            self.display_message("❌ Seleccione un rol para eliminar.", is_success=False)


    # ======================================================================
    # PESTAÑA DE USUARIOS
    # ======================================================================

    def _configurar_tab_usuarios(self, tab_frame: ctk.CTkFrame):
        tab_frame.columnconfigure(0, weight=1)
        tab_frame.columnconfigure(1, weight=1)
        tab_frame.rowconfigure(0, weight=1)

        # 1. Lista de Usuarios Existentes
        self.usuario_list_frame = ctk.CTkScrollableFrame(tab_frame, label_text="Usuarios Existentes", fg_color="#2e2e2e")
        self.usuario_list_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.usuario_list_frame.columnconfigure(0, weight=1)

        # 2. Formulario de Creación/Edición de Usuarios
        self.usuario_form_frame = ctk.CTkFrame(tab_frame, fg_color="#111111", corner_radius=10)
        self.usuario_form_frame.grid(row=0, column=1, sticky="nwe", padx=10, pady=10)
        self.usuario_form_frame.columnconfigure(0, weight=1)

        ctk.CTkLabel(self.usuario_form_frame, text="Gestión de Usuarios", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=15)

        # Documento
        ctk.CTkLabel(self.usuario_form_frame, text="Documento (ID único):").pack(padx=20, pady=(5, 0), fill="x")
        self.usuario_doc_entry = ctk.CTkEntry(self.usuario_form_frame, textvariable=self.usuario_doc_var)
        self.usuario_doc_entry.pack(padx=20, pady=(0, 10), fill="x")

        # Nombre
        ctk.CTkLabel(self.usuario_form_frame, text="Primer Nombre:").pack(padx=20, pady=(5, 0), fill="x")
        ctk.CTkEntry(self.usuario_form_frame, textvariable=self.usuario_nombre_var).pack(padx=20, pady=(0, 10), fill="x")
        
        # Apellido
        ctk.CTkLabel(self.usuario_form_frame, text="Apellido:").pack(padx=20, pady=(5, 0), fill="x")
        ctk.CTkEntry(self.usuario_form_frame, textvariable=self.usuario_apellido_var).pack(padx=20, pady=(0, 10), fill="x")

        # Rol
        ctk.CTkLabel(self.usuario_form_frame, text="Rol Asignado:").pack(padx=20, pady=(5, 0), fill="x")
        self.usuario_rol_combo = ctk.CTkComboBox(self.usuario_form_frame, 
                                                 variable=self.usuario_rol_var, 
                                                 values=["Seleccionar Rol"], # Se actualiza en _cargar_roles
                                                 height=35)
        self.usuario_rol_combo.pack(padx=20, pady=(0, 20), fill="x")

        # Botones de Acción
        btn_frame_user = ctk.CTkFrame(self.usuario_form_frame, fg_color="transparent")
        btn_frame_user.pack(padx=20, pady=(10, 20), fill="x")
        btn_frame_user.columnconfigure((0, 1), weight=1)
        
        self.btn_usuario_crear_guardar = ctk.CTkButton(btn_frame_user, text="➕ Crear Usuario", command=self._handle_usuario_save, 
                                                         fg_color="#2ecc71", hover_color="#27ae60", height=35)
        self.btn_usuario_crear_guardar.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        self.btn_usuario_cancelar = ctk.CTkButton(btn_frame_user, text="❌ Cancelar/Nuevo", command=lambda: self._limpiar_campos_usuario(clear_selection=True), 
                                                     fg_color="#e74c3c", hover_color="#c0392b", height=35)
        self.btn_usuario_cancelar.grid(row=0, column=1, padx=(5, 0), sticky="ew")

        self.btn_usuario_eliminar = ctk.CTkButton(self.usuario_form_frame, text="🗑️ Eliminar Usuario Seleccionado", command=self._handle_usuario_eliminar, 
                                                     fg_color="#c0392b", hover_color="#a0291a", height=35, state="disabled")
        self.btn_usuario_eliminar.pack(padx=20, pady=(10, 20), fill="x")


    def _cargar_usuarios(self, usuarios: List[Dict[str, Any]]):
        """Carga los usuarios en el marco de lista."""
        
        # Limpiar lista de usuarios
        for widget in self.usuario_list_frame.winfo_children():
            widget.destroy()
            
        for usuario in usuarios:
            # Crear elemento en la lista (visualización)
            user_frame = ctk.CTkFrame(self.usuario_list_frame, fg_color="#34495e", corner_radius=8)
            user_frame.pack(fill="x", padx=10, pady=(6, 3))
            
            ctk.CTkLabel(user_frame, text=f"{usuario['primer_nombre']} {usuario['apellido']} ({usuario['rol_nombre']})", 
                         font=ctk.CTkFont(size=14, weight="bold"), anchor="w").pack(padx=10, pady=(5, 0), fill="x")
            
            ctk.CTkLabel(user_frame, text=f"Doc: {usuario['documento']} | ID: {usuario['id']}", 
                         anchor="w", text_color="#bdc3c7").pack(padx=10, pady=(0, 5), fill="x")

            btn_edit = ctk.CTkButton(user_frame, text="Editar", width=60, 
                                     command=lambda u=usuario: self._cargar_usuario_para_edicion(u))
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
        
        opcion_a_seleccionar = f"{rol_id} - {rol_nombre}"
        
        combo_values = self.usuario_rol_combo.cget("values")
        if opcion_a_seleccionar in combo_values:
            self.usuario_rol_var.set(opcion_a_seleccionar)
        else:
            # Se usa el primer valor de la lista (normalmente "Seleccionar Rol") si el rol actual ya no existe
            self.usuario_rol_var.set(combo_values[0] if combo_values else "Seleccionar Rol")

        self.btn_usuario_crear_guardar.configure(text="💾 Guardar Cambios", fg_color="#3498db", hover_color="#2980b9")
        self.btn_usuario_eliminar.configure(state="normal")
        self.display_message(f"Cargado Usuario ID {usuario_data['id']} para edición.", True)

    def _limpiar_campos_usuario(self, clear_selection: bool = False):
        """Limpia los campos del formulario de Usuarios."""
        if clear_selection:
            self.usuario_id_var = None
        self.usuario_doc_var.set("")
        if self.usuario_doc_entry: # Comprobación de seguridad
            self.usuario_doc_entry.configure(state="normal") # Habilitar Documento para nuevo registro
        self.usuario_nombre_var.set("")
        self.usuario_apellido_var.set("")
        
        # Resetear el ComboBox al valor por defecto
        combo_values = self.usuario_rol_combo.cget("values") if self.usuario_rol_combo else []
        default_value = combo_values[0] if combo_values else "Seleccionar Rol"
        self.usuario_rol_var.set(default_value)
        
        self.btn_usuario_crear_guardar.configure(text="➕ Crear Usuario", fg_color="#2ecc71", hover_color="#27ae60")
        self.btn_usuario_eliminar.configure(state="disabled")
        self.display_message("Formulario de Usuario listo para un nuevo registro.", True)


    # --- Handlers de Usuario ---
    
    def _handle_usuario_save(self):
        """Maneja la creación o edición de un usuario."""
        rol_str = self.usuario_rol_var.get()
        rol_id = self.controller.get_rol_id_from_str(rol_str)
        
        data = {
            'id': self.usuario_id_var, # Será None si es creación
            'documento': self.usuario_doc_var.get().strip(),
            'primer_nombre': self.usuario_nombre_var.get().strip(),
            'apellido': self.usuario_apellido_var.get().strip(),
            'rol_id': rol_id,
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
            if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar al usuario '{nombre}' (ID: {self.usuario_id_var})?"):
                self.controller.handle_eliminar_usuario(self.usuario_id_var, nombre)
        else:
            self.display_message("❌ Seleccione un usuario para eliminar.", is_success=False)


    # ======================================================================
    # MÉTODO DE UTILIDAD
    # ======================================================================

    def display_message(self, message: str, is_success: bool = True):
        """Muestra un mensaje de estado en la interfaz."""
        color = "#2ecc71" if is_success else "#e74c3c"
        self.message_label.configure(text=message, text_color=color)


# --- Ejemplo de Ejecución (Opcional, para testear) ---
if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Sistema de Gestión - Configuración (Mock)")
    app.geometry("1000x700")

    controller = ConfiguracionControlador()
    view = ConfiguracionViewFrame(app, controller)
    view.pack(fill="both", expand=True)
    
    view.show() # Cargar datos iniciales
    
    app.mainloop()