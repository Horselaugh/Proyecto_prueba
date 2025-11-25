import customtkinter as ctk
from tkinter import messagebox
from typing import List, Dict
from controllers.relacion_controller import RelacionNNAFamiliarController
# Importar controladores para buscar NNA y Familiar
from controllers.nna_controller import NNAControlador
from controllers.familiar_controller import FamiliarControlador 

class RelacionNNAFamiliarViewFrame(ctk.CTkFrame):
    """
    Vista para gestionar la vinculación entre un NNA y un Familiar.
    """
    
    def __init__(self, master, controller: RelacionNNAFamiliarController):
        super().__init__(master, corner_radius=0, fg_color="transparent") 
        
        self.controller = controller 
        
        # Variables de control
        self.nna_id_var = ctk.StringVar(self)
        self.nna_nombre_var = ctk.StringVar(self, value="NNA no cargado")
        self.familiar_id_var = ctk.StringVar(self)
        self.familiar_nombre_var = ctk.StringVar(self, value="Familiar no cargado")
        self.parentesco_id_var = ctk.StringVar(self)
        self.convive_var = ctk.StringVar(self, value="Sí")
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1) 
        
        self._parentescos_map: Dict[str, int] = {} # Para mapear nombre a ID
        
        self._configurar_interfaz()

    # MÉTODO CLAVE
    def show(self):
        """Llamado por MenuApp, invoca la carga de datos iniciales."""
        self._cargar_parentescos()
        self.limpiar_entradas() 

    def _configurar_interfaz(self):
        """Configura la interfaz gráfica."""
        
        # Título y Mensaje
        self.title_label = ctk.CTkLabel(self, text="🔗 GESTIÓN DE VÍNCULOS NNA / FAMILIAR", 
                                         font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="ew")

        self.message_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14), text_color="yellow")
        self.message_label.grid(row=1, column=0, pady=5, padx=20, sticky="ew")

        # Contenedor principal de la relación
        form_frame = ctk.CTkFrame(self, fg_color="#3c3c3c", corner_radius=10, label_text="DATOS DEL VÍNCULO")
        form_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 10))
        form_frame.columnconfigure((0, 1), weight=1)
        
        # --- BÚSQUEDA Y CARGA (Izquierda) ---
        
        # Sección NNA
        nna_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        nna_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
        nna_frame.columnconfigure((0, 1), weight=1)
        
        ctk.CTkLabel(nna_frame, text="ID NNA:", font=("Arial", 14, "bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkEntry(nna_frame, textvariable=self.nna_id_var, placeholder_text="ID NNA", height=35).grid(row=1, column=0, sticky="ew", padx=(0, 5))
        ctk.CTkButton(nna_frame, text="Cargar NNA", command=lambda: self._simular_cargar_persona(self.nna_id_var.get(), 'NNA'), height=35).grid(row=1, column=1, sticky="ew", padx=(5, 0))
        ctk.CTkLabel(nna_frame, textvariable=self.nna_nombre_var, text_color="#3498db").grid(row=2, column=0, columnspan=2, sticky="w", pady=(5, 10))
        
        # Sección Familiar
        fam_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        fam_frame.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="ew")
        fam_frame.columnconfigure((0, 1), weight=1)
        
        ctk.CTkLabel(fam_frame, text="ID Familiar:", font=("Arial", 14, "bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkEntry(fam_frame, textvariable=self.familiar_id_var, placeholder_text="ID Familiar", height=35).grid(row=1, column=0, sticky="ew", padx=(0, 5))
        ctk.CTkButton(fam_frame, text="Cargar Familiar", command=lambda: self._simular_cargar_persona(self.familiar_id_var.get(), 'FAMILIAR'), height=35).grid(row=1, column=1, sticky="ew", padx=(5, 0))
        ctk.CTkLabel(fam_frame, textvariable=self.familiar_nombre_var, text_color="#2ecc71").grid(row=2, column=0, columnspan=2, sticky="w", pady=(5, 10))
        
        # --- CONFIGURACIÓN DEL VÍNCULO (Abajo) ---
        
        # Fila 1: Parentesco
        ctk.CTkLabel(form_frame, text="Parentesco:", font=("Arial", 14)).grid(row=3, column=0, sticky="w", padx=10, pady=(10, 5))
        self.parentesco_combo = ctk.CTkComboBox(form_frame, variable=self.parentesco_id_var, values=["Cargando..."], height=40)
        self.parentesco_combo.grid(row=4, column=0, sticky="ew", padx=10, pady=(0, 5))
        
        # Fila 2: Convive
        ctk.CTkLabel(form_frame, text="¿Conviven Juntos?:", font=("Arial", 14)).grid(row=3, column=1, sticky="w", padx=10, pady=(10, 5))
        ctk.CTkComboBox(form_frame, variable=self.convive_var, values=["Sí", "No"], height=40).grid(row=4, column=1, sticky="ew", padx=10, pady=(0, 5))
        
        # Botones de Acción
        ctk.CTkButton(form_frame, text="➕ Crear Vínculo", command=self._handle_crear_relacion, height=45, 
                      fg_color="#3498db", hover_color="#2980b9", font=ctk.CTkFont(size=16, weight="bold")).grid(row=5, column=0, columnspan=2, padx=10, pady=(20, 10), sticky="ew")
        
        # --- LISTADO DE RELACIONES (Parte inferior) ---
        
        list_frame = ctk.CTkFrame(self, fg_color="#3c3c3c", corner_radius=10, label_text="RELACIONES DEL NNA CARGADO")
        list_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 20))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        self.listado_text = ctk.CTkTextbox(list_frame, wrap="word", height=150, state="disabled")
        self.listado_text.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nsew")
        
        self.btn_listar_relaciones = ctk.CTkButton(list_frame, text="Mostrar Relaciones", command=self._handle_listar_relaciones, height=35, state="disabled")
        self.btn_listar_relaciones.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

    # ----------------------------------------------------------------------
    # Handlers y Lógica de Negocio
    # ----------------------------------------------------------------------
    
    def _simular_cargar_persona(self, persona_id_str, tipo: str):
        """
        Simula la carga de datos de NNA o Familiar. 
        NOTA: En un sistema real, esto llamaría a NNAControlador.cargar_nna()
        o FamiliarControlador.cargar_familiar().
        """
        try:
            p_id = int(persona_id_str)
            if p_id <= 0:
                raise ValueError
            
            # SIMULACIÓN (Reemplazar por llamada a controlador real)
            nombre = f"Persona {p_id} ({tipo})" 
            
            if tipo == 'NNA':
                self.nna_nombre_var.set(nombre)
                self.btn_listar_relaciones.configure(state="normal")
                self.display_message(f"NNA ID {p_id} cargado.", is_success=True)
                self._handle_listar_relaciones() # Listar al cargar NNA
            elif tipo == 'FAMILIAR':
                self.familiar_nombre_var.set(nombre)
                self.display_message(f"Familiar ID {p_id} cargado.", is_success=True)

        except ValueError:
            self.display_message(f"❌ Ingrese un ID numérico válido para {tipo}.", is_success=False)
            if tipo == 'NNA':
                self.nna_nombre_var.set("NNA no cargado")
                self.btn_listar_relaciones.configure(state="disabled")
            elif tipo == 'FAMILIAR':
                self.familiar_nombre_var.set("Familiar no cargado")

    def _cargar_parentescos(self):
        """Carga los valores de Parentesco desde el controlador."""
        parentescos = self.controller.obtener_parentescos_disponibles()
        
        nombres = []
        self._parentescos_map = {}
        
        for id, nombre in parentescos:
            nombres.append(nombre)
            self._parentescos_map[nombre] = id
            
        if nombres:
            self.parentesco_combo.configure(values=nombres)
            self.parentesco_id_var.set(nombres[0])
        else:
            self.parentesco_combo.configure(values=["No hay parentescos"])
            self.parentesco_id_var.set("No hay parentescos")

    def _handle_crear_relacion(self):
        """Maneja la creación del vínculo NNA-Familiar."""
        
        nna_id_str = self.nna_id_var.get().strip()
        familiar_id_str = self.familiar_id_var.get().strip()
        parentesco_nombre = self.parentesco_id_var.get().strip()
        convive = self.convive_var.get()
        
        try:
            nna_id = int(nna_id_str)
            familiar_id = int(familiar_id_str)
            parentesco_id = self._parentescos_map.get(parentesco_nombre)
            
            if not parentesco_id:
                self.display_message("❌ Seleccione un tipo de parentesco válido.", is_success=False)
                return

            exito, mensaje = self.controller.crear_nueva_relacion(nna_id, familiar_id, parentesco_id, convive)
            self.display_message(mensaje, is_success=exito)
            
            if exito:
                self._handle_listar_relaciones() # Actualizar la lista
                
        except ValueError:
            self.display_message("❌ Asegúrese de que ambos IDs (NNA y Familiar) sean números enteros.", is_success=False)
        except Exception as e:
            self.display_message(f"❌ Error desconocido al crear relación: {e}", is_success=False)

    def _handle_listar_relaciones(self):
        """Obtiene y muestra la lista de relaciones para el NNA cargado."""
        nna_id_str = self.nna_id_var.get().strip()
        try:
            nna_id = int(nna_id_str)
        except ValueError:
            self.display_message("❌ No hay un ID de NNA válido cargado para listar relaciones.", is_success=False)
            self._actualizar_listado_relaciones([])
            return
            
        relaciones = self.controller.listar_relaciones_de_nna(nna_id)
        self._actualizar_listado_relaciones(relaciones)
        
    def _actualizar_listado_relaciones(self, relaciones: List[Dict]):
        """Actualiza el widget de texto con la lista de relaciones."""
        self.listado_text.configure(state="normal")
        self.listado_text.delete("1.0", "end")
        
        if not relaciones:
            self.listado_text.insert("end", "No hay vínculos registrados para este NNA.")
        else:
            header = "{:<5} {:<25} {:<15} {:<10}\n".format("ID FAM", "FAMILIAR", "PARENTESCO", "¿CONVIVE?")
            self.listado_text.insert("end", header, "header")
            self.listado_text.insert("end", "-" * 55 + "\n")
            
            for r in relaciones:
                convive_str = "Sí" if r['convive'] else "No"
                linea = "{:<5} {:<25} {:<15} {:<10}\n".format(
                    r['familiar_id'], 
                    r['nombre_familiar'], 
                    r['parentesco'], 
                    convive_str
                )
                self.listado_text.insert("end", linea)

        self.listado_text.configure(state="disabled")

    def limpiar_entradas(self):
        """Limpia todos los campos de la relación."""
        self.nna_id_var.set("")
        self.nna_nombre_var.set("NNA no cargado")
        self.familiar_id_var.set("")
        self.familiar_nombre_var.set("Familiar no cargado")
        self.convive_var.set("Sí")
        
        if self._parentescos_map:
            self.parentesco_id_var.set(list(self._parentescos_map.keys())[0])
        
        self.btn_listar_relaciones.configure(state="disabled")
        self._actualizar_listado_relaciones([])
        self.display_message("")
        
    def display_message(self, message: str, is_success: bool = True):
        """Muestra un mensaje de estado en la interfaz."""
        color = "#2ecc71" if is_success else "#e74c3c"
        self.message_label.configure(text=message, text_color=color)