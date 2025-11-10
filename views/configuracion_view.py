import customtkinter as ctk
import tkinter.messagebox as messagebox
import sys
import os

# Agregar las carpetas al path de Python
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'controllers'))

from configuracion_controller import ConfiguracionController

class ConfiguracionView:
    """
    Vista para el módulo de configuración usando CustomTkinter
    """
    
    def __init__(self, root):
        self.root = root
        self.controller = ConfiguracionController()
        
        self.rol_seleccionado = None
        self.usuario_seleccionado = None
        
        self._configurar_interfaz()
        self._cargar_datos()
    
    def _configurar_interfaz(self):
        """Configura la interfaz gráfica"""
        self.root.title("Módulo de Configuración")
        self.root.geometry("800x600")  # Aumentar el tamaño de la ventana
        
        # Hacer que la ventana sea redimensionable
        self.root.minsize(800, 600)
        
        self.title_label = ctk.CTkLabel(self.root, text="Módulo de Configuración",
                                        font=("Arial", 20, "bold"))
        self.title_label.pack(pady=10)

        self.tabview = ctk.CTkTabview(self.root, width=780, height=520)  # Aumentar tamaño
        self.tabview.pack(padx=10, pady=10, fill="both", expand=True)  # Hacer que se expanda

        self.tabview.add("Roles")
        self.tabview.add("Usuarios")

        self._configurar_tab_roles()
        self._configurar_tab_usuarios()
    
    def _configurar_tab_roles(self):
        """Configura la pestaña de Roles"""
        tab = self.tabview.tab("Roles")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=2)
        tab.grid_rowconfigure(0, weight=1)  # Hacer que la fila se expanda

        # Frame para lista de roles con scroll
        self.roles_frame = ctk.CTkScrollableFrame(tab, width=280, height=400)
        self.roles_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Frame para controles con scroll
        controls_container = ctk.CTkFrame(tab)
        controls_container.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        controls_container.grid_columnconfigure(0, weight=1)
        controls_container.grid_rowconfigure(0, weight=1)

        # Frame scrollable para los controles
        controls_frame = ctk.CTkScrollableFrame(controls_container, width=450, height=400)
        controls_frame.grid(row=0, column=0, sticky="nsew")
        controls_frame.grid_columnconfigure(0, weight=1)

        # Función de validación para solo letras y espacios
        def validar_solo_letras(texto):
            """Valida que el texto contenga solo letras y espacios"""
            if texto == "":
                return True
            # Permite letras, espacios, y algunos caracteres especiales comunes en nombres
            return all(c.isalpha() or c.isspace() or c in "áéíóúÁÉÍÓÚñÑ" for c in texto)
        
        vcmd_letras = (self.root.register(validar_solo_letras), '%P')

        # Campos para rol
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

        # Botones - colocados en la parte inferior
        btn_frame = ctk.CTkFrame(controls_frame)
        btn_frame.grid(row=4, column=0, padx=10, pady=20, sticky="ew")
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)

        self.btn_crear_rol = ctk.CTkButton(btn_frame, text="Crear Rol",
                                        command=self._crear_rol)
        self.btn_crear_rol.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.btn_guardar_rol = ctk.CTkButton(btn_frame, text="Guardar Cambios", 
                                            command=self._guardar_rol, state="disabled")
        self.btn_guardar_rol.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.btn_eliminar_rol = ctk.CTkButton(btn_frame, text="Eliminar Rol",
                                            command=self._eliminar_rol,
                                            state="disabled", fg_color="red")
        self.btn_eliminar_rol.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        # Asegurar que la columna se expanda
        controls_frame.grid_columnconfigure(0, weight=1)
    
    def _configurar_tab_usuarios(self):
        """Configura la pestaña de Usuarios"""
        tab = self.tabview.tab("Usuarios")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=2)
        tab.grid_rowconfigure(0, weight=1)  # Hacer que la fila se expanda

        # Frame para lista de usuarios con scroll
        self.usuarios_frame = ctk.CTkScrollableFrame(tab, width=280, height=400)
        self.usuarios_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Frame para controles con scroll
        controls_container = ctk.CTkFrame(tab)
        controls_container.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        controls_container.grid_columnconfigure(0, weight=1)
        controls_container.grid_rowconfigure(0, weight=1)

        # Frame scrollable para los controles
        controls_frame = ctk.CTkScrollableFrame(controls_container, width=450, height=400)
        controls_frame.grid(row=0, column=0, sticky="nsew")
        controls_frame.grid_columnconfigure(0, weight=1)

        # Función de validación para solo letras y espacios
        def validar_solo_letras(texto):
            """Valida que el texto contenga solo letras y espacios"""
            if texto == "":
                return True
            # Permite letras, espacios, y algunos caracteres especiales comunes en nombres
            return all(c.isalpha() or c.isspace() or c in "áéíóúÁÉÍÓÚñÑ" for c in texto)
        
        # Función de validación para documento de identidad (solo números)
        def validar_solo_numeros(texto):
            """Valida que el texto contenga solo números"""
            if texto == "":
                return True
            return texto.isdigit()
        
        # Función de validación para dirección (más permisiva)
        def validar_direccion(texto):
            """Valida que el texto sea una dirección válida"""
            if texto == "":
                return True
            # Permite letras, números, espacios y caracteres comunes en direcciones
            caracteres_permitidos = "áéíóúÁÉÍÓÚñÑ#-.,"
            return all(c.isalnum() or c.isspace() or c in caracteres_permitidos for c in texto)
        
        vcmd_letras = (self.root.register(validar_solo_letras), '%P')
        vcmd_numeros = (self.root.register(validar_solo_numeros), '%P')
        vcmd_direccion = (self.root.register(validar_direccion), '%P')

        # Campos para usuario
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

        # Selector de rol
        ctk.CTkLabel(controls_frame, text="Rol:", 
                    font=("Arial", 12, "bold")).grid(row=12, column=0, padx=10, pady=(10, 5), sticky="w")
        
        self.rol_optionmenu = ctk.CTkOptionMenu(controls_frame, values=[])
        self.rol_optionmenu.grid(row=13, column=0, padx=10, pady=(0, 20), sticky="ew")

        # Botones - colocados en la parte inferior
        btn_frame = ctk.CTkFrame(controls_frame)
        btn_frame.grid(row=14, column=0, padx=10, pady=20, sticky="ew")
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)

        self.btn_crear_usuario = ctk.CTkButton(btn_frame, text="Crear Usuario", 
                                              command=self._crear_usuario)
        self.btn_crear_usuario.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.btn_guardar_usuario = ctk.CTkButton(btn_frame, text="Guardar Cambios", 
                                                command=self._guardar_usuario, state="disabled")
        self.btn_guardar_usuario.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.btn_eliminar_usuario = ctk.CTkButton(btn_frame, text="Eliminar Usuario", 
                                                 command=self._eliminar_usuario, 
                                                 state="disabled", fg_color="red")
        self.btn_eliminar_usuario.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        # Tooltip informativo
        info_label = ctk.CTkLabel(
            controls_frame, 
            text="ℹ️ Campos de nombre y apellido: solo letras | Documento: solo números",
            text_color="gray",
            font=ctk.CTkFont(size=11)
        )
        info_label.grid(row=15, column=0, padx=10, pady=10, sticky="w")
        
        # Asegurar que la columna se expanda
        controls_frame.grid_columnconfigure(0, weight=1)
    
    def _cargar_datos(self):
        """Carga los datos iniciales"""
        self._actualizar_vista_roles()
        self._actualizar_vista_usuarios()
        self._actualizar_opciones_roles()
    
    def _actualizar_vista_roles(self):
        """Actualiza la vista de roles"""
        for widget in self.roles_frame.winfo_children():
            widget.destroy()
        
        roles = self.controller.obtener_roles()
        for rol in roles:
            btn = ctk.CTkButton(
                self.roles_frame, 
                text=rol['nombre'],
                command=lambda r=rol: self._seleccionar_rol(r)
            )
            btn.pack(fill="x", pady=2)
    
    def _actualizar_vista_usuarios(self):
        """Actualiza la vista de usuarios"""
        for widget in self.usuarios_frame.winfo_children():
            widget.destroy()
        
        usuarios = self.controller.obtener_usuarios()
        for usuario in usuarios:
            texto_boton = f"{usuario['nombre_usuario']} {usuario['primer_apellido']}"
            btn = ctk.CTkButton(
                self.usuarios_frame, 
                text=texto_boton,
                command=lambda u=usuario: self._seleccionar_usuario(u)
            )
            btn.pack(fill="x", pady=2)
    
    def _actualizar_opciones_roles(self):
        """Actualiza las opciones de roles en el selector"""
        roles = self.controller.obtener_roles()
        nombres_roles = [rol['nombre'] for rol in roles]
        self.rol_optionmenu.configure(values=nombres_roles)
        if nombres_roles:
            self.rol_optionmenu.set(nombres_roles[0])
    
    def _seleccionar_rol(self, rol):
        """Maneja la selección de un rol"""
        self.rol_seleccionado = rol
        self.rol_nombre_entry.delete(0, "end")
        self.rol_descripcion_entry.delete(0, "end")
        
        # CORREGIDO: Usar str() para evitar errores con CustomTkinter
        if rol['nombre']:
            self.rol_nombre_entry.insert(0, str(rol['nombre']))
        if rol.get('descripcion'):
            self.rol_descripcion_entry.insert(0, str(rol.get('descripcion', '')))
        
        self.btn_guardar_rol.configure(state="normal")
        self.btn_eliminar_rol.configure(state="normal")
    
    def _seleccionar_usuario(self, usuario):
        """Maneja la selección de un usuario"""
        self.usuario_seleccionado = usuario
        
        # Limpiar campos
        for entry_name in ['primer_nombre_entry', 'segundo_nombre_entry',
                        'primer_apellido_entry', 'segundo_apellido_entry',
                        'documento_entry', 'direccion_entry']:
            entry = getattr(self, entry_name)
            entry.delete(0, "end")
        
        # CORREGIDO: Usar str() para evitar errores con CustomTkinter
        if usuario.get('nombre_usuario'):
            self.primer_nombre_entry.insert(0, str(usuario.get('nombre_usuario', '')))
        if usuario.get('segundo_nombre'):
            self.segundo_nombre_entry.insert(0, str(usuario.get('segundo_nombre', '')))
        if usuario.get('primer_apellido'):
            self.primer_apellido_entry.insert(0, str(usuario.get('primer_apellido', '')))
        if usuario.get('segundo_apellido'):
            self.segundo_apellido_entry.insert(0, str(usuario.get('segundo_apellido', '')))
        if usuario.get('documento_identidad'):
            self.documento_entry.insert(0, str(usuario.get('documento_identidad', '')))
        if usuario.get('direccion'):
            self.direccion_entry.insert(0, str(usuario.get('direccion', '')))
        
        if usuario.get('rol_nombre'):
            self.rol_optionmenu.set(str(usuario.get('rol_nombre', '')))
        
        self.btn_guardar_usuario.configure(state="normal")
        self.btn_eliminar_usuario.configure(state="normal")
    
    def _crear_rol(self):
        """Crea un nuevo rol"""
        nombre = self.rol_nombre_entry.get().strip()
        descripcion = self.rol_descripcion_entry.get().strip()
        
        if self.controller.crear_rol(nombre, descripcion):
            self._limpiar_campos_rol()
            self._actualizar_vista_roles()
            self._actualizar_opciones_roles()
    
    def _guardar_rol(self):
        """Guarda los cambios de un rol"""
        if not self.rol_seleccionado:
            return
        
        nuevo_nombre = self.rol_nombre_entry.get().strip()
        nueva_descripcion = self.rol_descripcion_entry.get().strip()
        
        if self.controller.actualizar_rol(
            self.rol_seleccionado['id'], nuevo_nombre, nueva_descripcion
        ):
            self._limpiar_campos_rol()
            self._actualizar_vista_roles()
            self._actualizar_opciones_roles()
            self._deshabilitar_botones_rol()
    
    def _eliminar_rol(self):
        """Elimina el rol seleccionado"""
        if not self.rol_seleccionado:
            return
        
        if self.controller.eliminar_rol(
            self.rol_seleccionado['id'], self.rol_seleccionado['nombre']
        ):
            self._limpiar_campos_rol()
            self._actualizar_vista_roles()
            self._actualizar_opciones_roles()
            self._deshabilitar_botones_rol()
    
    def _crear_usuario(self):
        """Crea un nuevo usuario"""
        # Validación adicional antes de crear
        if not self._validar_campos_usuario():
            return
        
        # Obtener rol seleccionado
        rol_nombre = self.rol_optionmenu.get()
        roles = self.controller.obtener_roles()
        rol_id = next((r['id'] for r in roles if r['nombre'] == rol_nombre), None)
        
        datos_usuario = {
            'primer_nombre': self.primer_nombre_entry.get().strip(),
            'segundo_nombre': self.segundo_nombre_entry.get().strip(),
            'primer_apellido': self.primer_apellido_entry.get().strip(),
            'segundo_apellido': self.segundo_apellido_entry.get().strip(),
            'documento_identidad': self.documento_entry.get().strip(),
            'direccion': self.direccion_entry.get().strip(),
            'rol_id': rol_id
        }
        
        if self.controller.crear_usuario(datos_usuario):
            self._limpiar_campos_usuario()
            self._actualizar_vista_usuarios()
    
    def _guardar_usuario(self):
        """Guarda los cambios de un usuario"""
        if not self.usuario_seleccionado:
            return
        
        # Validación adicional antes de guardar
        if not self._validar_campos_usuario():
            return
        
        # Obtener rol seleccionado
        rol_nombre = self.rol_optionmenu.get()
        roles = self.controller.obtener_roles()
        rol_id = next((r['id'] for r in roles if r['nombre'] == rol_nombre), None)
        
        datos_usuario = {
            'persona_id': self.usuario_seleccionado['persona_id'],
            'primer_nombre': self.primer_nombre_entry.get().strip(),
            'segundo_nombre': self.segundo_nombre_entry.get().strip(),
            'primer_apellido': self.primer_apellido_entry.get().strip(),
            'segundo_apellido': self.segundo_apellido_entry.get().strip(),
            'documento_identidad': self.documento_entry.get().strip(),
            'direccion': self.direccion_entry.get().strip(),
            'nombre_usuario_anterior': self.usuario_seleccionado.get('nombre_usuario', ''),
            'rol_id': rol_id
        }
        
        if self.controller.actualizar_usuario(datos_usuario):
            self._limpiar_campos_usuario()
            self._actualizar_vista_usuarios()
    
    def _eliminar_usuario(self):
        """Elimina el usuario seleccionado"""
        if not self.usuario_seleccionado:
            return
        
        if self.controller.eliminar_usuario(
            self.usuario_seleccionado['persona_id'], 
            self.usuario_seleccionado['nombre_usuario']
        ):
            self._limpiar_campos_usuario()
            self._actualizar_vista_usuarios()
    
    def _validar_campos_usuario(self):
        """Valida los campos del usuario antes de guardar"""
        # Validar que los campos de nombre y apellido contengan solo letras
        def contiene_solo_letras(texto):
            return all(c.isalpha() or c.isspace() or c in "áéíóúÁÉÍÓÚñÑ" for c in texto)
        
        campos_texto = [
            (self.primer_nombre_entry.get(), "Primer Nombre"),
            (self.segundo_nombre_entry.get(), "Segundo Nombre"),
            (self.primer_apellido_entry.get(), "Primer Apellido"),
            (self.segundo_apellido_entry.get(), "Segundo Apellido")
        ]
        
        for valor, nombre_campo in campos_texto:
            if valor and not contiene_solo_letras(valor):
                messagebox.showerror("Error", f"El campo '{nombre_campo}' solo puede contener letras")
                return False
        
        # Validar que el documento contenga solo números
        documento = self.documento_entry.get()
        if documento and not documento.isdigit():
            messagebox.showerror("Error", "El campo 'Documento de Identidad' solo puede contener números")
            return False
        
        return True
    
    def _limpiar_campos_rol(self):
        """Limpia los campos de rol"""
        self.rol_nombre_entry.delete(0, "end")
        self.rol_descripcion_entry.delete(0, "end")
    
    def _limpiar_campos_usuario(self):
        """Limpia los campos de usuario"""
        for entry_name in ['primer_nombre_entry', 'segundo_nombre_entry',
                          'primer_apellido_entry', 'segundo_apellido_entry',
                          'documento_entry', 'direccion_entry']:
            entry = getattr(self, entry_name)
            entry.delete(0, "end")
    
    def _deshabilitar_botones_rol(self):
        """Deshabilita los botones de rol"""
        self.btn_guardar_rol.configure(state="disabled")
        self.btn_eliminar_rol.configure(state="disabled")
        self.rol_seleccionado = None