# views/funcion_vista_tercero.py

import customtkinter as ctk
from tkinter import messagebox
from typing import Optional, List
from controllers.tercero_controller import TerceroController
import datetime

# ----------------------------------------------------------------------
# VISTA: GESTIÓN DE TERCEROS
# ----------------------------------------------------------------------

class TerceroViewFrame(ctk.CTkFrame):
    """
    Vista para el módulo de gestión de Terceros (Vecinos, Docentes, Entidades). 
    """
    
    def __init__(self, master, controller: TerceroController):
        super().__init__(master, corner_radius=0, fg_color="transparent") 
        
        self.controller = controller 
        # No hay necesidad de registrar la vista en el controlador si este no la manipula
        
        # Variables de control del formulario
        self.doc_id_var = ctk.StringVar(self)
        self.p_nombre_var = ctk.StringVar(self)
        self.s_nombre_var = ctk.StringVar(self)
        self.p_apellido_var = ctk.StringVar(self)
        self.s_apellido_var = ctk.StringVar(self)
        self.genero_var = ctk.StringVar(self)
        self.telefono_var = ctk.StringVar(self)
        self.direccion_var = ctk.StringVar(self)
        self.relacion_var = ctk.StringVar(self) # NUEVA variable para Terceros
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1) 
        
        self._configurar_interfaz()

    # MÉTODO CLAVE: Requerido por la estructura de menu.py
    def show(self):
        """Llamado por MenuApp, invoca la carga de datos iniciales."""
        self._cargar_catalogos()
        self.listar_terceros() # Llamar a listar al mostrar la vista

    def _configurar_interfaz(self):
        """Configura la interfaz gráfica (Diseño General)."""
        
        # Título y Mensaje
        self.title_label = ctk.CTkLabel(self, text="👨‍🏫 GESTIÓN DE TERCEROS", 
                                         font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="ew")

        self.message_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14), text_color="yellow")
        self.message_label.grid(row=1, column=0, pady=5, padx=20, sticky="ew")

        # Contenedor principal
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        main_container.columnconfigure(0, weight=1) # Formulario (izquierda)
        main_container.columnconfigure(1, weight=2) # Listado (derecha)
        main_container.rowconfigure(0, weight=1)
        
        # --- IZQUIERDA: Formulario de Registro ---
        form_frame = ctk.CTkScrollableFrame(main_container, fg_color="#111111", corner_radius=10, label_text="REGISTRO DE TERCERO")
        form_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)
        form_frame.columnconfigure(0, weight=1)
        
        # Campos del Formulario (Similar a NNA)
        
        # Fila 1: Nombres
        self._add_field(form_frame, 0, 0, "Primer Nombre (Obligatorio):", self.p_nombre_var)
        self._add_field(form_frame, 2, 0, "Segundo Nombre:", self.s_nombre_var)
        
        # Fila 2: Apellidos
        self._add_field(form_frame, 4, 0, "Primer Apellido (Obligatorio):", self.p_apellido_var)
        self._add_field(form_frame, 6, 0, "Segundo Apellido:", self.s_apellido_var)
        
        # Fila 3: Cédula/Identificación y Género
        self._add_field(form_frame, 8, 0, "Documento de Identidad (Obligatorio):", self.doc_id_var)
        self._add_field(form_frame, 10, 0, "Género (M/F):", self.genero_var, is_combo=True, combo_values=["M", "F"])
        
        # Fila 4: Teléfono y Relación NNA (Catálogo)
        self._add_field(form_frame, 12, 0, "Teléfono (Obligatorio):", self.telefono_var)
        self._add_field(form_frame, 14, 0, "Tipo de Relación NNA:", self.relacion_var, is_combo=True)
        
        # Fila 5: Dirección
        self._add_field(form_frame, 16, 0, "Dirección (Obligatoria):", self.direccion_var)

        # Botón de Creación y Limpiar
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=18, column=0, padx=10, pady=(20, 10), sticky="ew")
        
        ctk.CTkButton(button_frame, text="➕ Registrar Tercero", command=self._handle_crear_tercero, height=45, 
                      fg_color="#2ecc71", hover_color="#27ae60", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", expand=True, fill="x", padx=5)
        
        ctk.CTkButton(button_frame, text="🧹 Limpiar", command=self.limpiar_entradas, height=45, 
                      fg_color="#95a5a6", hover_color="#7f8c8d", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", expand=True, fill="x", padx=5)
                      
        # --- DERECHA: Listado de Terceros (Tabla) ---
        list_frame = ctk.CTkFrame(main_container, fg_color="#111111", corner_radius=10, border_width=1)
        list_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=0)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(1, weight=1)
        
        ctk.CTkLabel(list_frame, text="LISTA DE TERCEROS REGISTRADOS", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=(10, 5), padx=10, sticky="ew")
        
        # Creación del Treeview (Simulado por un Text/ScrollableFrame)
        self.listado_text = ctk.CTkTextbox(list_frame, wrap="word", height=200, state="disabled")
        self.listado_text.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        
        ctk.CTkButton(list_frame, text="🔄 Recargar Lista", command=self.listar_terceros, height=35).grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")


    def _add_field(self, parent, row, column, label_text, var, is_combo=False, combo_values=None):
        """Función auxiliar para añadir etiquetas y campos de entrada/combobox."""
        ctk.CTkLabel(parent, text=label_text, font=("Arial", 14)).grid(row=row, column=column, sticky="w", padx=10, pady=(10, 5))
        
        if is_combo:
            combo = ctk.CTkComboBox(parent, variable=var, values=combo_values if combo_values else ["Cargando..."], height=40)
            combo.grid(row=row + 1, column=column, sticky="ew", padx=10, pady=(0, 5))
            # Guardar referencia a la combo box de relación si es el caso
            if label_text == "Tipo de Relación NNA:":
                 self.relacion_combo = combo
            if label_text == "Género (M/F):":
                 self.genero_combo = combo
        else:
            ctk.CTkEntry(parent, textvariable=var, height=40).grid(row=row + 1, column=column, sticky="ew", padx=10, pady=(0, 5))
            
    # ----------------------------------------------------------------------
    # Handlers y Lógica de Negocio
    # ----------------------------------------------------------------------
    
    def _handle_crear_tercero(self):
        data = self._obtener_datos_formulario()
        exito, mensaje = self.controller.registrar_tercero(data)
        
        self.display_message(mensaje, is_success=exito)
        if exito:
            self.limpiar_entradas()
            self.listar_terceros() # Actualizar la lista al crear
            
    def _obtener_datos_formulario(self): 
        """Recolecta los datos de los campos de entrada."""
        return {
            "documento_identidad": self.doc_id_var.get().strip(),
            "primer_nombre": self.p_nombre_var.get().strip(),
            "segundo_nombre": self.s_nombre_var.get().strip() or None,
            "primer_apellido": self.p_apellido_var.get().strip(),
            "segundo_apellido": self.s_apellido_var.get().strip() or None,
            "genero": self.genero_var.get().strip(),
            "direccion": self.direccion_var.get().strip(),
            "telefono": self.telefono_var.get().strip(),
            "relacion_nna": self.relacion_var.get().strip()
        }
    
    def limpiar_entradas(self): 
        """Limpia todos los campos del formulario."""
        self.doc_id_var.set("")
        self.p_nombre_var.set("")
        self.s_nombre_var.set("")
        self.p_apellido_var.set("")
        self.s_apellido_var.set("")
        self.telefono_var.set("")
        self.direccion_var.set("")
        
        # Resetear ComboBoxes al primer valor
        if hasattr(self, 'genero_combo') and self.genero_combo.cget("values"):
             self.genero_var.set(self.genero_combo.cget("values")[0])
        if hasattr(self, 'relacion_combo') and self.relacion_combo.cget("values"):
             self.relacion_var.set(self.relacion_combo.cget("values")[0])
             
        self.display_message("")

    def _cargar_catalogos(self):
        """Carga los valores de los ComboBoxes de catálogos."""
        # Cargar Relaciones NNA
        relaciones = self.controller.obtener_lista_relaciones()
        if hasattr(self, 'relacion_combo') and relaciones:
            self.relacion_combo.configure(values=relaciones)
            self.relacion_var.set(relaciones[0])
            
        # Cargar Géneros (Ya configurado con valores fijos ["M", "F"] en _add_field, pero se podría sobreescribir si el catálogo viniera de DB)
        
    def listar_terceros(self):
        """Obtiene y muestra la lista de terceros en el Textbox."""
        terceros = self.controller.listar_terceros()
        
        self.listado_text.configure(state="normal")
        self.listado_text.delete("1.0", "end")
        
        if not terceros:
            self.listado_text.insert("end", "No hay terceros registrados aún.")
        else:
            header = "{:<5} {:<15} {:<25} {:<15}\n".format("ID", "IDENTIDAD", "NOMBRE COMPLETO", "RELACIÓN")
            self.listado_text.insert("end", header, "header")
            self.listado_text.insert("end", "-" * 60 + "\n")
            
            for t in terceros:
                nombre_completo = f"{t['primer_nombre']} {t['primer_apellido']}"
                linea = "{:<5} {:<15} {:<25} {:<15}\n".format(
                    t['id'], 
                    t['documento_identidad'] or 'N/A', 
                    nombre_completo, 
                    t['relacion_nna']
                )
                self.listado_text.insert("end", linea)

        self.listado_text.configure(state="disabled")
        
    def display_message(self, message: str, is_success: bool = True):
        """Muestra un mensaje de estado en la interfaz."""
        color = "#2ecc71" if is_success else "#e74c3c"
        self.message_label.configure(text=message, text_color=color)