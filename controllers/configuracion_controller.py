import customtkinter as ctk
import sys
import os

# Eliminamos la importación del controlador y de messagebox.
# La Vista NO debe conocer ni crear su propio controlador, ni manejar errores.

class ConfiguracionView:
    """
    Vista para el módulo de configuración usando CustomTkinter.
    Se enfoca únicamente en la presentación y la recolección de entrada del usuario.
    Delega toda la lógica de negocio y la validación al controlador.
    """
    
    def __init__(self, root, controller):
        # El constructor recibe el controlador inyectado (Inversión de Control)
        self.root = root
        self.controller = controller 
        
        self.rol_seleccionado = None
        self.usuario_seleccionado = None
        
        self._configurar_interfaz()
        # Llamar al controlador para cargar los datos iniciales
        self.controller.load_initial_data() 
    
    def _configurar_interfaz(self):
        """Configura la interfaz gráfica"""
        self.root.title("Módulo de Configuración")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        
        self.title_label = ctk.CTkLabel(self.root, text="Módulo de Configuración",
                                        font=("Arial", 20, "bold"))
        self.title_label.pack(pady=10)

        # Etiqueta central de mensajes (para que el Controlador se comunique con el usuario)
        self.message_label = ctk.CTkLabel(self.root, text="", font=("Arial", 12))
        self.message_label.pack(pady=5)
        
        self.tabview = ctk.CTkTabview(self.root, width=780, height=520)
        self.tabview.pack(padx=10, pady=10, fill="both", expand=True)

        self.tabview.add("Roles")
        self.tabview.add("Usuarios")

        self._configurar_tab_roles()
        self._configurar_tab_usuarios()
    
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
        
        # Validación de entrada para retroalimentación inmediata (NO ES LÓGICA DE NEGOCIO)
        def validar_solo_letras(texto):
            if texto == "": return True
            # Permite letras, espacios y caracteres acentuados comunes en español
            return all(c.isalpha() or c.isspace() or c in "áéíóúÁÉÍÓÚñÑ" for c in texto)
        vcmd_letras = (self.root.register(validar_solo_letras), '%P')

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

        # Los comandos llaman a los métodos de acción de la Vista para delegar
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

        # Funciones de validación de entrada para retroalimentación inmediata
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
        
        vcmd_letras = (self.root.register(validar_solo_letras), '%P')
        vcmd_numeros = (self.root.register(validar_solo_numeros), '%P')
        vcmd_direccion = (self.root.register(validar_direccion), '%P')

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

        # Los comandos llaman a los métodos de acción de la Vista para delegar
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
        """Recopila datos y delega la acción al controlador."""
        nombre = self.rol_nombre_entry.get().strip()
        descripcion = self.rol_descripcion_entry.get().strip()
        
        self.controller.handle_crear_rol(nombre, descripcion)
    
    def _handle_guardar_rol(self):
        """Recopila datos y delega la acción al controlador."""
        if not self.rol_seleccionado:
            self.display_message("Error: Debe seleccionar un rol para guardar cambios.", is_success=False)
            return
            
        rol_id = self.rol_seleccionado.get('id')
        nuevo_nombre = self.rol_nombre_entry.get().strip()
        nueva_descripcion = self.rol_descripcion_entry.get().strip()
        
        self.controller.handle_guardar_rol(rol_id, nuevo_nombre, nueva_descripcion)
    
    def _handle_eliminar_rol(self):
        """Recopila datos y delega la acción al controlador."""
        if not self.rol_seleccionado:
            self.display_message("Error: Debe seleccionar un rol para eliminar.", is_success=False)
            return
            
        rol_id = self.rol_seleccionado.get('id')
        nombre = self.rol_seleccionado.get('nombre')

        self.controller.handle_eliminar_rol(rol_id, nombre)
        
    def _get_usuario_data(self):
        """Método helper para obtener los datos del formulario de usuario."""
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
        """Recopila datos y delega la acción al controlador."""
        datos_usuario = self._get_usuario_data()
        self.controller.handle_crear_usuario(datos_usuario)
    
    def _handle_guardar_usuario(self):
        """Recopila datos y delega la acción al controlador."""
        if not self.usuario_seleccionado:
            self.display_message("Error: Debe seleccionar un usuario para guardar cambios.", is_success=False)
            return
        
        datos_usuario = self._get_usuario_data()
        self.controller.handle_guardar_usuario(datos_usuario)

    def _handle_eliminar_usuario(self):
        """Recopila datos y delega la acción al controlador."""
        if not self.usuario_seleccionado:
            self.display_message("Error: Debe seleccionar un usuario para eliminar.", is_success=False)
            return
            
        persona_id = self.usuario_seleccionado.get('persona_id')
        nombre_usuario = self.usuario_seleccionado.get('nombre_usuario')

        self.controller.handle_eliminar_usuario(persona_id, nombre_usuario)

    # --- MÉTODOS DE MANIPULACIÓN DE UI (Invocados por el Controlador) ---

    def _seleccionar_rol(self, rol):
        """Maneja la selección de un rol para la edición."""
        self.rol_seleccionado = rol
        self._limpiar_campos_rol()
        
        if rol:
            # Rellenar campos
            self.rol_nombre_entry.insert(0, str(rol['nombre']))
            self.rol_descripcion_entry.insert(0, str(rol.get('descripcion', '')))
            self.btn_guardar_rol.configure(state="normal")
            self.btn_eliminar_rol.configure(state="normal")
        else:
             self._deshabilitar_botones_rol()
    
    def _seleccionar_usuario(self, usuario):
        """Maneja la selección de un usuario para la edición."""
        self.usuario_seleccionado = usuario
        self._limpiar_campos_usuario()
        
        if usuario:
            # Rellenar campos
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
        """Método público para que el Controlador muestre un mensaje al usuario."""
        color = "green" if is_success else "red"
        self.message_label.configure(text=message, text_color=color)

    def set_roles_list(self, roles):
        """Actualiza la lista de roles en la pestaña de Roles."""
        for widget in self.roles_frame.winfo_children():
            widget.destroy()
        
        for rol in roles:
            # El botón llama al método de la vista, que delega la acción al controlador
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

    def set_usuarios_list(self, usuarios):
        """Actualiza la lista de usuarios en la pestaña de Usuarios."""
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

    def _limpiar_campos_rol(self):
        """Limpia los campos de rol."""
        self.rol_nombre_entry.delete(0, "end")
        self.rol_descripcion_entry.delete(0, "end")
        self.rol_seleccionado = None
    
    def _limpiar_campos_usuario(self):
        """Limpia los campos de usuario."""
        for entry_name in ['primer_nombre_entry', 'segundo_nombre_entry',
                          'primer_apellido_entry', 'segundo_apellido_entry',
                          'documento_entry', 'direccion_entry']:
            entry = getattr(self, entry_name)
            entry.delete(0, "end")
        self.usuario_seleccionado = None
    
    def _deshabilitar_botones_rol(self):
        """Deshabilita los botones de rol."""
        self.btn_guardar_rol.configure(state="disabled")
        self.btn_eliminar_rol.configure(state="disabled")
        self.rol_seleccionado = None
        self._limpiar_campos_rol()

    def _deshabilitar_botones_usuario(self):
        """Deshabilita los botones de usuario."""
        self.btn_guardar_usuario.configure(state="disabled")
        self.btn_eliminar_usuario.configure(state="disabled")
        self.usuario_seleccionado = None
        self._limpiar_campos_usuario()