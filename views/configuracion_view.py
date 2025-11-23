import customtkinter as ctk
import sys
import os


# ----------------------------------------------------------------------
# MOCK DE MODELO (TEMPORAL)
# ----------------------------------------------------------------------

# 🔴 MOCK TEMPORAL: Necesario para que el Controlador pueda inicializar su propiedad 'modelo'
class MockConfiguracionModelo:
    def get_all_roles(self): return [{"id": 1, "nombre": "Admin", "descripcion": "Administrador"}]
    def get_all_usuarios(self): return []
    def handle_crear_rol(self, *args): return True
    def handle_guardar_rol(self, *args): return True
    def handle_eliminar_rol(self, *args): return True
    def handle_crear_usuario(self, *args): return True
    def handle_guardar_usuario(self, *args): return True
    def handle_eliminar_usuario(self, *args): return True


class ConfiguracionViewFrame(ctk.CTkFrame):
    """
    Vista para el módulo de configuración. 
    Hereda de CTkFrame para ser cargado en el panel de contenido.
    """
    
    # Recibe 'master' (el CTkFrame de contenido de MenuApp) y 'controller' (ConfiguracionControlador)
    def __init__(self, master, controller):
        super().__init__(master, corner_radius=0, fg_color="transparent") 
        
        self.controller = controller 
        # 🔴 CORRECCIÓN: La Vista se registra en el Controlador para que este pueda actualizarla
        self.controller.set_view(self) 
        
        self.rol_seleccionado = None
        self.usuario_seleccionado = None
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self._configurar_interfaz()
        
    def _configurar_interfaz(self):
        """Configura la interfaz gráfica dentro de este frame."""
        
        # Contenedor principal
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_container.grid_rowconfigure(2, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        
        self.title_label = ctk.CTkLabel(main_container, text="Módulo de Configuración",
                                        font=("Arial", 20, "bold"))
        self.title_label.grid(row=0, column=0, pady=(0, 10), sticky="n")

        # Etiqueta central de mensajes 
        self.message_label = ctk.CTkLabel(main_container, text="", font=("Arial", 12))
        self.message_label.grid(row=1, column=0, pady=5, sticky="n")
        
        self.tabview = ctk.CTkTabview(main_container, width=780, height=520)
        self.tabview.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.tabview.add("Roles")
        self.tabview.add("Usuarios")

        self._configurar_tab_roles()
        self._configurar_tab_usuarios()
        
    def show(self):
        """MÉTODO CLAVE: Llamado por MenuApp, invoca la carga de datos del controlador."""
        self.controller.load_initial_data() 
        
    # El resto de métodos de la vista son correctos y se omiten para brevedad.
    # ... (Se omiten los métodos _configurar_tab_roles, _configurar_tab_usuarios, _handle_crear_rol, etc.)

    def _configurar_tab_roles(self):
        tab = self.tabview.tab("Roles")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=2)
        tab.grid_rowconfigure(0, weight=1)

        self.roles_frame = ctk.CTkScrollableFrame(tab, width=280, height=400)
        self.roles_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        controls_container = ctk.CTkFrame(tab)
        controls_container.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        controls_container.grid_columnconfigure(0, weight=1)
        controls_container.grid_rowconfigure(0, weight=1)

        controls_frame = ctk.CTkScrollableFrame(controls_container, width=450, height=400)
        controls_frame.grid(row=0, column=0, sticky="nsew")
        controls_frame.grid_columnconfigure(0, weight=1)
        
        # Obtener la ventana raíz para el registro de comandos (importante)
        root_window = self.winfo_toplevel() 
        
        def validar_solo_letras(texto):
            if texto == "": return True
            return all(c.isalpha() or c.isspace() or c in "áéíóúÁÉÍÓÚñÑ" for c in texto)
        
        # Usamos el registro de la ventana principal
        vcmd_letras = (root_window.register(validar_solo_letras), '%P')

        ctk.CTkLabel(controls_frame, text="Nombre del Rol:", 
                    font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        
        self.rol_nombre_entry = ctk.CTkEntry(
            controls_frame, 
            placeholder_text="Nombre del rol",
            validate="key",
            validatecommand=vcmd_letras
        )
        self.rol_nombre_entry.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        
        ctk.CTkLabel(controls_frame, text="Descripción:", 
                    font=("Arial", 12, "bold")).grid(row=2, column=0, padx=10, pady=(10, 5), sticky="w")
        
        self.rol_descripcion_entry = ctk.CTkEntry(controls_frame, placeholder_text="Descripción del rol")
        self.rol_descripcion_entry.grid(row=3, column=0, padx=10, pady=(0, 20), sticky="ew")

        btn_frame = ctk.CTkFrame(controls_frame)
        btn_frame.grid(row=4, column=0, padx=10, pady=20, sticky="ew")
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)

        self.btn_crear_rol = ctk.CTkButton(btn_frame, text="Crear Rol",
                                        command=self._handle_crear_rol)
        self.btn_crear_rol.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.btn_guardar_rol = ctk.CTkButton(btn_frame, text="Guardar Cambios", 
                                            command=self._handle_guardar_rol, state="disabled")
        self.btn_guardar_rol.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.btn_eliminar_rol = ctk.CTkButton(btn_frame, text="Eliminar Rol",
                                            command=self._handle_eliminar_rol,
                                            state="disabled", fg_color="red")
        self.btn_eliminar_rol.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        controls_frame.grid_columnconfigure(0, weight=1)

    def _configurar_tab_usuarios(self):
        tab = self.tabview.tab("Usuarios")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=2)
        tab.grid_rowconfigure(0, weight=1)

        self.usuarios_frame = ctk.CTkScrollableFrame(tab, width=280, height=400)
        self.usuarios_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        controls_container = ctk.CTkFrame(tab)
        controls_container.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        controls_container.grid_columnconfigure(0, weight=1)
        controls_container.grid_rowconfigure(0, weight=1)

        controls_frame = ctk.CTkScrollableFrame(controls_container, width=450, height=400)
        controls_frame.grid(row=0, column=0, sticky="nsew")
        controls_frame.grid_columnconfigure(0, weight=1)

        root_window = self.winfo_toplevel()
        
        # Funciones de validación de entrada
        def validar_solo_letras(texto):
            if texto == "": return True
            return all(c.isalpha() or c.isspace() or c in "áéíóúÁÉÍÓÚñÑ" for c in texto)
        def validar_solo_numeros(texto):
            if texto == "": return True
            return texto.isdigit()
        def validar_direccion(texto):
            if texto == "": return True
            caracteres_permitidos = "áéíóúÁÉÍÓÚñÑ#-.,"
            return all(c.isalnum() or c.isspace() or c in caracteres_permitidos for c in texto)
        
        vcmd_letras = (root_window.register(validar_solo_letras), '%P')
        vcmd_numeros = (root_window.register(validar_solo_numeros), '%P')
        vcmd_direccion = (root_window.register(validar_direccion), '%P')

        campos = [
            ("Primer Nombre:", "primer_nombre_entry", vcmd_letras),
            ("Segundo Nombre:", "segundo_nombre_entry", vcmd_letras),
            ("Primer Apellido:", "primer_apellido_entry", vcmd_letras),
            ("Segundo Apellido:", "segundo_apellido_entry", vcmd_letras),
            ("Documento de Identidad:", "documento_entry", vcmd_numeros),
            ("Dirección:", "direccion_entry", vcmd_direccion)
        ]
        
        for i, (texto, nombre, validacion) in enumerate(campos):
            ctk.CTkLabel(controls_frame, text=texto, 
                        font=("Arial", 12, "bold")).grid(row=i*2, column=0, padx=10, pady=(10, 5), sticky="w")
            
            entry = ctk.CTkEntry(
                controls_frame, 
                placeholder_text=texto.replace(":", ""),
                validate="key",
                validatecommand=validacion
            )
            entry.grid(row=i*2+1, column=0, padx=10, pady=(0, 10), sticky="ew")
            setattr(self, nombre, entry)

        ctk.CTkLabel(controls_frame, text="Rol:", 
                    font=("Arial", 12, "bold")).grid(row=12, column=0, padx=10, pady=(10, 5), sticky="w")
        
        self.rol_optionmenu = ctk.CTkOptionMenu(controls_frame, values=[])
        self.rol_optionmenu.grid(row=13, column=0, padx=10, pady=(0, 20), sticky="ew")

        btn_frame = ctk.CTkFrame(controls_frame)
        btn_frame.grid(row=14, column=0, padx=10, pady=20, sticky="ew")
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)

        self.btn_crear_usuario = ctk.CTkButton(btn_frame, text="Crear Usuario", 
                                              command=self._handle_crear_usuario)
        self.btn_crear_usuario.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.btn_guardar_usuario = ctk.CTkButton(btn_frame, text="Guardar Cambios", 
                                                command=self._handle_guardar_usuario, state="disabled")
        self.btn_guardar_usuario.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.btn_eliminar_usuario = ctk.CTkButton(btn_frame, text="Eliminar Usuario", 
                                                 command=self._handle_eliminar_usuario, 
                                                 state="disabled", fg_color="red")
        self.btn_eliminar_usuario.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        info_label = ctk.CTkLabel(
            controls_frame, 
            text="ℹ️ Campos de nombre y apellido: solo letras | Documento: solo números",
            text_color="gray",
            font=ctk.CTkFont(size=11)
        )
        info_label.grid(row=15, column=0, padx=10, pady=10, sticky="w")
        
        controls_frame.grid_columnconfigure(0, weight=1)


    # --- MÉTODOS DE ACCIÓN (Delegación pura al Controlador) ---
    def _handle_crear_rol(self):
        nombre = self.rol_nombre_entry.get().strip()
        descripcion = self.rol_descripcion_entry.get().strip()
        self.controller.handle_crear_rol(nombre, descripcion)
    
    def _handle_guardar_rol(self):
        if not self.rol_seleccionado:
            self.display_message("Error: Debe seleccionar un rol para guardar cambios.", is_success=False)
            return
        rol_id = self.rol_seleccionado.get('id')
        nuevo_nombre = self.rol_nombre_entry.get().strip()
        nueva_descripcion = self.rol_descripcion_entry.get().strip()
        self.controller.handle_guardar_rol(rol_id, nuevo_nombre, nueva_descripcion)
    
    def _handle_eliminar_rol(self):
        if not self.rol_seleccionado:
            self.display_message("Error: Debe seleccionar un rol para eliminar.", is_success=False)
            return
        rol_id = self.rol_seleccionado.get('id')
        nombre = self.rol_seleccionado.get('nombre')
        self.controller.handle_eliminar_rol(rol_id, nombre)
        
    def _get_usuario_data(self):
        rol_nombre = self.rol_optionmenu.get()
        return {
            'persona_id': self.usuario_seleccionado.get('persona_id') if self.usuario_seleccionado else None,
            'rol_nombre': rol_nombre,
            'primer_nombre': self.primer_nombre_entry.get().strip(),
            'segundo_nombre': self.segundo_nombre_entry.get().strip(),
            'primer_apellido': self.primer_apellido_entry.get().strip(),
            'segundo_apellido': self.segundo_apellido_entry.get().strip(),
            'documento_identidad': self.documento_entry.get().strip(),
            'direccion': self.direccion_entry.get().strip(),
            'nombre_usuario_anterior': self.usuario_seleccionado.get('nombre_usuario', '') if self.usuario_seleccionado else ''
        }
    
    def _handle_crear_usuario(self):
        datos_usuario = self._get_usuario_data()
        self.controller.handle_crear_usuario(datos_usuario)
    
    def _handle_guardar_usuario(self):
        if not self.usuario_seleccionado:
            self.display_message("Error: Debe seleccionar un usuario para guardar cambios.", is_success=False)
            return
        datos_usuario = self._get_usuario_data()
        self.controller.handle_guardar_usuario(datos_usuario)

    def _handle_eliminar_usuario(self):
        if not self.usuario_seleccionado:
            self.display_message("Error: Debe seleccionar un usuario para eliminar.", is_success=False)
            return
        persona_id = self.usuario_seleccionado.get('persona_id')
        nombre_usuario = self.usuario_seleccionado.get('nombre_usuario')
        self.controller.handle_eliminar_usuario(persona_id, nombre_usuario)

    # --- MÉTODOS DE MANIPULACIÓN DE UI (Invocados por el Controlador) ---
    def _seleccionar_rol(self, rol):
        self.rol_seleccionado = rol
        self._limpiar_campos_rol(clear_selection=False)
        if rol:
            self.rol_nombre_entry.insert(0, str(rol['nombre']))
            self.rol_descripcion_entry.insert(0, str(rol.get('descripcion', '')))
            self.btn_guardar_rol.configure(state="normal")
            self.btn_eliminar_rol.configure(state="normal")
        else:
             self._deshabilitar_botones_rol()
    
    def _seleccionar_usuario(self, usuario):
        self.usuario_seleccionado = usuario
        self._limpiar_campos_usuario(clear_selection=False)
        if usuario:
            self.primer_nombre_entry.insert(0, str(usuario.get('primer_nombre', '')))
            self.segundo_nombre_entry.insert(0, str(usuario.get('segundo_nombre', '')))
            self.primer_apellido_entry.insert(0, str(usuario.get('primer_apellido', '')))
            self.segundo_apellido_entry.insert(0, str(usuario.get('segundo_apellido', '')))
            self.documento_entry.insert(0, str(usuario.get('documento_identidad', '')))
            self.direccion_entry.insert(0, str(usuario.get('direccion', '')))
            if usuario.get('rol_nombre'):
                self.rol_optionmenu.set(str(usuario.get('rol_nombre', '')))
            self.btn_guardar_usuario.configure(state="normal")
            self.btn_eliminar_usuario.configure(state="normal")
        else:
            self._deshabilitar_botones_usuario()

    def display_message(self, message, is_success=True):
        color = "green" if is_success else "red"
        self.message_label.configure(text=message, text_color=color)

    def set_roles_list(self, roles):
        for widget in self.roles_frame.winfo_children():
            widget.destroy()
        
        for rol in roles:
            btn = ctk.CTkButton(
                self.roles_frame, 
                text=rol['nombre'],
                command=lambda r=rol: self._seleccionar_rol(r)
            )
            btn.pack(fill="x", pady=2)
        
        nombres_roles = [rol['nombre'] for rol in roles]
        self.rol_optionmenu.configure(values=nombres_roles)
        if nombres_roles:
            self.rol_optionmenu.set(nombres_roles[0])
        
        self._limpiar_campos_rol(clear_selection=True)

    def set_usuarios_list(self, usuarios):
        for widget in self.usuarios_frame.winfo_children():
            widget.destroy()
        
        for usuario in usuarios:
            texto_boton = f"{usuario.get('primer_nombre', 'N/A')} {usuario.get('primer_apellido', 'N/A')}"
            btn = ctk.CTkButton(
                self.usuarios_frame, 
                text=texto_boton,
                command=lambda u=usuario: self._seleccionar_usuario(u)
            )
            btn.pack(fill="x", pady=2)
            
        self._limpiar_campos_usuario(clear_selection=True)

    def _limpiar_campos_rol(self, clear_selection=True):
        self.rol_nombre_entry.delete(0, "end")
        self.rol_descripcion_entry.delete(0, "end")
        if clear_selection:
            self.rol_seleccionado = None
            self._deshabilitar_botones_rol()
    
    def _limpiar_campos_usuario(self, clear_selection=True):
        for entry_name in ['primer_nombre_entry', 'segundo_nombre_entry',
                          'primer_apellido_entry', 'segundo_apellido_entry',
                          'documento_entry', 'direccion_entry']:
            entry = getattr(self, entry_name)
            entry.delete(0, "end")
        if clear_selection:
            self.usuario_seleccionado = None
            self._deshabilitar_botones_usuario()
    
    def _deshabilitar_botones_rol(self):
        self.btn_guardar_rol.configure(state="disabled")
        self.btn_eliminar_rol.configure(state="disabled")
        self.rol_seleccionado = None

    def _deshabilitar_botones_usuario(self):
        self.btn_guardar_usuario.configure(state="disabled")
        self.btn_eliminar_usuario.configure(state="disabled")
        self.usuario_seleccionado = None

# ----------------------------------------------------------------------
# CLASE DE CONTROLADOR
# ----------------------------------------------------------------------

class ConfiguracionControlador:
    """
    Controlador que maneja la interacción entre el Modelo y la Vista.
    Instanciado por MenuApp, y responsable de crear la vista.
    """
    
    # 🔴 CORRECCIÓN: Agregar __init__ para instanciar el Modelo (Mock/Real) y gestionar la Vista
    def __init__(self):
        # Aquí debería ir la importación e instanciación del Modelo real.
        self.modelo = MockConfiguracionModelo() 
        self.vista = None

    def set_view(self, view_instance):
        """Asigna la instancia de la vista al controlador."""
        self.vista = view_instance
        
    def get_view(self):
        """Método requerido por MenuApp para obtener el frame de la vista."""
        return self.vista

    def load_initial_data(self):
        """
        MÉTODO CLAVE: Contiene la lógica para cargar datos iniciales.
        Llamado por MenuApp a través de vista.show().
        """
        if not self.vista:
            print("ERROR CRÍTICO: El controlador de configuración se llamó sin una vista asignada.")
            return

        self.vista.display_message("Cargando datos de configuración...", is_success=True)
        try:
            roles = self.modelo.get_all_roles()
            usuarios = self.modelo.get_all_usuarios()
            
            self.vista.set_roles_list(roles)
            self.vista.set_usuarios_list(usuarios)
            self.vista.display_message("Datos de configuración cargados correctamente. ✅", is_success=True)
            
        except Exception as e:
             self.vista.display_message(f"❌ Error al cargar datos: {e}", is_success=False)

    # --- MÉTODOS DE NEGOCIO (Handlers para la Vista) ---
    
    def handle_crear_rol(self, nombre, descripcion):
        if self.modelo.handle_crear_rol(nombre, descripcion):
            self.vista.display_message(f"✅ Rol '{nombre}' creado.", is_success=True)
            self.load_initial_data() 
        else:
            self.vista.display_message(f"❌ Error al crear el rol: {nombre}.", is_success=False)
            
    def handle_guardar_rol(self, rol_id, nuevo_nombre, nueva_descripcion):
        if self.modelo.handle_guardar_rol(rol_id, nuevo_nombre, nueva_descripcion):
            self.vista.display_message(f"✅ Rol '{nuevo_nombre}' modificado.", is_success=True)
            self.load_initial_data() 
        else:
            self.vista.display_message(f"❌ Error al modificar el rol: {nuevo_nombre}.", is_success=False)

    def handle_eliminar_rol(self, rol_id, nombre):
        if self.modelo.handle_eliminar_rol(rol_id):
            self.vista.display_message(f"🗑️ Rol '{nombre}' eliminado.", is_success=True)
            self.vista._limpiar_campos_rol(clear_selection=True)
            self.load_initial_data() 
        else:
            self.vista.display_message(f"❌ Error al eliminar el rol: {nombre}.", is_success=False)

    def _validar_usuario_data(self, data):
        # Implementación de validación básica
        if not all([data['primer_nombre'], data['documento_identidad']]):
            self.vista.display_message("❌ Error: Nombre y documento son obligatorios.", is_success=False)
            return False
        return True

    def handle_crear_usuario(self, data):
        if not self._validar_usuario_data(data): return
        if self.modelo.handle_crear_usuario(data):
            self.vista.display_message(f"✅ Usuario {data['primer_nombre']} creado.", is_success=True)
            self.vista._limpiar_campos_usuario(clear_selection=True)
            self.load_initial_data()
        else:
            self.vista.display_message(f"❌ Error al crear usuario.", is_success=False)

    def handle_guardar_usuario(self, data):
        if not self._validar_usuario_data(data): return
        if self.modelo.handle_guardar_usuario(data):
            self.vista.display_message(f"✅ Usuario {data['primer_nombre']} guardado.", is_success=True)
            self.vista._limpiar_campos_usuario(clear_selection=True)
            self.load_initial_data()
        else:
            self.vista.display_message(f"❌ Error al guardar usuario.", is_success=False)

    def handle_eliminar_usuario(self, persona_id, nombre_usuario):
        if self.modelo.handle_eliminar_usuario(persona_id):
            self.vista.display_message(f"🗑️ Usuario {nombre_usuario} eliminado.", is_success=True)
            self.vista._limpiar_campos_usuario(clear_selection=True)
            self.load_initial_data()
        else:
            self.vista.display_message(f"❌ Error al eliminar usuario.", is_success=False)