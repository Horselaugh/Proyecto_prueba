import sys
import os
import customtkinter
import tkinter as tk
from tkinter import messagebox

# Asegurarse de importar ttk (Treeview)
try:
    from tkinter import ttk
except ImportError:
    import tkinter.ttk as ttk
    
from tooltip import ToolTip

# Esto es necesario para que el script principal pueda encontrar el módulo
sys.path.append(os.path.join(os.path.dirname(__file__))) 

class FuncionVistaDenuncia(customtkinter.CTkFrame):
    """
    Vista para el módulo de gestión de Denuncias.
    Utiliza el patrón de delegación para que los eventos de la UI llamen a métodos de la vista, 
    y estos a su vez llamen a métodos del controlador con los datos correctos.
    """
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)

        self.controller = controller
        # Se registra la vista en el controlador si este patrón se usa (como en ArticuloControlador)
        # self.controller.set_view(self) # Descomentar si el controlador lo requiere
        
        # --- Configuración del Grid Principal de la Vista ---
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # 1. CREACIÓN DEL FRAME CONTENEDOR PRINCIPAL
        self.frame = customtkinter.CTkFrame(
            master=self,
            corner_radius=10
        )
        self.frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Configuración del grid dentro del frame
        self.frame.grid_columnconfigure(0, weight=1)
        for i in range(1, 5):
            self.frame.grid_rowconfigure(i, weight=0)
        self.frame.grid_rowconfigure(5, weight=1) 
        
        # 2. AÑADIR EL CTkLABEL PARA EL TÍTULO
        self.label_titulo = customtkinter.CTkLabel(
            master=self.frame,
            text="Gestión de Denuncias",
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.label_titulo.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w") 

        # --- Variables de Búsqueda y Filtrado ---
        self.entry_busqueda_var = tk.StringVar(value="")
        self.filtro_estado_var = tk.StringVar(value="Todos")
        
        # --- Widget de Búsqueda ---
        self.entry_busqueda = customtkinter.CTkEntry(
            master=self.frame,
            placeholder_text="Buscar por nombre o descripción...",
            textvariable=self.entry_busqueda_var,
            width=300
        )
        self.entry_busqueda.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        # DELEGACIÓN: Enlazar la pulsación de tecla al método de la VISTA
        self.entry_busqueda.bind("<KeyRelease>", self._handle_busqueda_o_filtro)
        
        # --- Dropdown de Filtrado por Estado ---
        estados = ["Todos", "Pendiente", "En Revisión", "Resuelto", "Rechazado"]
        self.dropdown_filtro_estado = customtkinter.CTkOptionMenu(
            master=self.frame,
            values=estados,
            variable=self.filtro_estado_var,
            # DELEGACIÓN: Enlazar el cambio de valor al método de la VISTA
            command=self._handle_busqueda_o_filtro, 
            width=150
        )
        self.dropdown_filtro_estado.grid(row=1, column=0, padx=(330, 20), pady=10, sticky="w")
        
        # --- Botones de Acción ---
        
        # Botón para crear nueva denuncia
        self.boton_nueva_denuncia = customtkinter.CTkButton(
            master=self.frame,
            text="Nueva Denuncia",
            command=self.mostrar_formulario_crear,
            fg_color="#00C853",
            hover_color="#00A040"
        )
        self.boton_nueva_denuncia.grid(row=2, column=0, padx=20, pady=(10, 5), sticky="w")
        ToolTip(self.boton_nueva_denuncia, "Crear un nuevo registro de denuncia")

        # Botón para generar reporte
        self.boton_reporte = customtkinter.CTkButton(
            master=self.frame,
            text="Generar Reporte",
            # Se asume que el método del controlador puede aceptar argumentos opcionales (*args)
            command=self.controller.generar_reporte_denuncias, 
            fg_color="#1E88E5",
            hover_color="#1565C0"
        )
        self.boton_reporte.grid(row=2, column=0, padx=(190, 0), pady=(10, 5), sticky="w")
        ToolTip(self.boton_reporte, "Exportar el listado actual a un archivo (ej. PDF/Excel)")

        # --- Tabla de Denuncias (Treeview) ---
        columnas = ("id", "nombre", "estado", "fecha", "acciones")
        self.tabla_denuncias = ttk.Treeview(
            master=self.frame,
            columns=columnas,
            show="headings"
        )
        
        # Estilos y Encabezados
        style = ttk.Style()
        style.theme_use("clam")
        
        # Configurar las columnas
        self.tabla_denuncias.heading("id", text="ID", anchor=tk.CENTER)
        self.tabla_denuncias.heading("nombre", text="Título de Denuncia", anchor=tk.W)
        self.tabla_denuncias.heading("estado", text="Estado", anchor=tk.CENTER)
        self.tabla_denuncias.heading("fecha", text="Fecha", anchor=tk.CENTER)
        self.tabla_denuncias.heading("acciones", text="Acciones", anchor=tk.CENTER)
        
        self.tabla_denuncias.column("id", width=50, stretch=tk.NO, anchor=tk.CENTER)
        self.tabla_denuncias.column("nombre", width=300, stretch=tk.YES, anchor=tk.W)
        self.tabla_denuncias.column("estado", width=120, stretch=tk.NO, anchor=tk.CENTER)
        self.tabla_denuncias.column("fecha", width=120, stretch=tk.NO, anchor=tk.CENTER)
        self.tabla_denuncias.column("acciones", width=100, stretch=tk.NO, anchor=tk.CENTER)

        # Scrollbar vertical
        self.scrollbar = customtkinter.CTkScrollbar(
            master=self.frame, 
            command=self.tabla_denuncias.yview
        )
        self.tabla_denuncias.configure(yscrollcommand=self.scrollbar.set)
        
        self.tabla_denuncias.grid(row=5, column=0, padx=(20, 0), pady=10, sticky="nsew")
        self.scrollbar.grid(row=5, column=0, padx=(0, 20), pady=10, sticky="nse")

        # Bind para doble clic en la tabla (para editar/ver detalles)
        self.tabla_denuncias.bind("<Double-1>", self.on_double_click_tabla)

        # Cargar datos iniciales (Ahora llama a la vista, no directamente al controlador sin argumentos)
        # self.controller.actualizar_tabla() # LÍNEA ORIGINAL ELIMINADA
        self._handle_busqueda_o_filtro()
        
    # --- Métodos de la Vista (Delegación) ---
    
    def show(self):
        """Llamado por la aplicación principal para asegurar que la tabla se cargue al mostrarse."""
        self._handle_busqueda_o_filtro() 
        
    def _handle_busqueda_o_filtro(self, event=None):
        """
        Recolecta los datos de búsqueda y filtro y llama al método del controlador 
        con el diccionario de argumentos correcto.
        
        :param event: Argumento posicional opcional recibido de bind o command.
        """
        datos_busqueda = {
            'texto': self.entry_busqueda_var.get(),
            'estado': self.filtro_estado_var.get()
        }
        
        # El controlador devuelve la lista de datos, la vista los inserta en la tabla
        datos = self.controller.actualizar_tabla(datos_busqueda)
        self.cargar_datos_en_tabla(datos)

    # --- Métodos de la Vista (Implementación) ---

    def mostrar_formulario_crear(self):
        # Lógica para mostrar el formulario de creación
        pass
        
    def on_double_click_tabla(self, event):
        # Lógica para manejar el doble clic en la tabla
        pass

    def cargar_datos_en_tabla(self, datos: list):
        """Limpia el Treeview e inserta los nuevos datos."""
        # Limpiar datos anteriores
        for item in self.tabla_denuncias.get_children():
            self.tabla_denuncias.delete(item)
            
        # Insertar nuevos datos
        for row in datos:
            # Asumiendo que 'row' es un diccionario con las claves 'id', 'nombre', 'estado', 'fecha'
            self.tabla_denuncias.insert('', 'end', values=(
                row.get('id', ''), 
                row.get('nombre', 'N/A'), 
                row.get('estado', 'N/A'), 
                row.get('fecha', 'N/A'), 
                'Ver/Editar' # Columna de acciones
            ))

    def mostrar_mensaje(self, titulo, mensaje):
        # Lógica para mostrar mensajes al usuario
        messagebox.showinfo(titulo, mensaje)