import customtkinter as ctk
from tkinter import ttk, messagebox
from typing import List, Dict, Optional, Any
# Aunque Pylance reportó un error con pandas, lo mantenemos si el plan es usarlo para exportar.
# Si el entorno no lo tiene, solo el mock de exportación funcionará.
try:
    import pandas as pd
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    CAN_PLOT = True
except ImportError:
    # Si falta pandas o matplotlib, deshabilitamos la funcionalidad de gráfico.
    CAN_PLOT = False
    
import datetime

# ======================================================================
# MOCK del Controlador (Añadido get_expediente_id_from_str)
# ======================================================================
class MockControlador:
    def __init__(self): self.vista = None
    def set_view(self, view_instance): self.vista = view_instance
    
    def get_expedientes_para_reportes(self) -> List[Dict[str, Any]]:
        """Mock: Retorna una lista de expedientes para filtros y reportes."""
        return [
            {"id": 10, "descripcion": "10 - Caso NNA Juan P. (Abierto)"},
            {"id": 15, "descripcion": "15 - Caso NNA María L. (Cerrado)"},
            {"id": 20, "descripcion": "20 - Caso Familia S. (Abierto)"},
        ]
    
    def get_expediente_id_from_str(self, exp_str: str) -> Optional[int]:
        """
        Mock: Extrae el ID numérico del expediente desde la cadena (e.g., '10 - Caso...')
        Este es el método que faltaba y ha sido añadido.
        """
        if exp_str is None or exp_str == "Todos":
            return None
        try:
            # Asume que el ID está al inicio, antes del primer espacio o guión
            return int(exp_str.split(' - ')[0].split(' ')[0])
        except (ValueError, IndexError):
            # Si la cadena no tiene el formato esperado
            return None
        
    def load_initial_data(self):
        if self.vista:
            reportes = {"NNA_GENERAL": "Reporte General de NNA", "NNA_POR_GENERO": "NNA por Género (Gráfico)"}
            self.vista._cargar_reportes_disponibles(reportes)
            self.vista.display_stats({'total_nna': 100, 'alertas_activas': 5, 'fecha_actualizacion': 'Hoy'})
            # Cargar los expedientes al iniciar la vista
            expedientes = self.get_expedientes_para_reportes()
            self.vista._cargar_opciones_filtros(expedientes) 
            
    def handle_generar_reporte(self, reporte_key: str, filtros: Dict[str, Any]):
        self.vista.display_message(f"Mock: Generando reporte '{reporte_key}' con filtros: {filtros}", True)

        if reporte_key == "NNA_POR_GENERO" and CAN_PLOT:
            # Simular datos para el gráfico de barras
            self.vista._plot_chart("bar_genero", {'Femenino': 60, 'Masculino': 40, 'Otro': 0})
            self.vista.display_results([], [], "Gráfico Generado")
        elif reporte_key == "NNA_GENERAL":
            # Simular datos tabulares
            mock_data = [
                {'ID': 10, 'NNA': 'Juan Pérez', 'Género': 'Masculino', 'Estado': 'Activo'},
                {'ID': 15, 'NNA': 'María López', 'Género': 'Femenino', 'Estado': 'Cerrado'}
            ]
            columnas = list(mock_data[0].keys()) if mock_data else []
            self.vista._mostrar_resultados_tabla(mock_data, columnas, "Reporte General generado.")
        else:
            self.vista.display_message(f"Mock: Reporte '{reporte_key}' generado. (Datos no tabulares simulados)", True)

    def handle_exportar_reporte(self, data, columns):
        # El Mock solo muestra un mensaje, pero el método ahora recibe los datos
        if data:
            self.vista.display_message(f"Mock: Exportando {len(data)} filas de datos...", True)
        else:
            self.vista.display_message("Mock: No hay datos para exportar.", False)


# Importamos el controlador (o su mock)
try:
    from controllers.reportes_controller import ReportesControlador
except ImportError:
    ReportesControlador = MockControlador


class ReportesViewFrame(ctk.CTkFrame):
    """
    Vista para el módulo de Reportes.
    Hereda de CTkFrame para ser cargado en el panel de contenido.
    """

    def __init__(self, master, controller: MockControlador):
        super().__init__(master, corner_radius=0, fg_color="transparent") 
        
        self.controller = controller 
        self.controller.set_view(self) 
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1) 
        
        # Variables de control
        self.reporte_key_var = ctk.StringVar(self, value="Seleccionar Reporte")
        self.filtro_exp_var = ctk.StringVar(self, value="Todos")
        self.filtro_desde_var = ctk.StringVar(self, value="")
        self.filtro_hasta_var = ctk.StringVar(self, value="")
        
        # Almacena el widget de canvas para poder destruirlo
        self.canvas_widget: Optional[ctk.CTkWidget] = None
        # Almacena los últimos datos generados para la exportación
        self.last_report_data: List[Dict] = []
        self.last_report_columns: List[str] = []
        
        self._configurar_interfaz()

    def show(self):
        """Llamado por MenuApp, invoca la carga de datos iniciales del controlador."""
        self.controller.load_initial_data() 

    def _configurar_interfaz(self):
        """Configura la interfaz gráfica."""
        
        # Título y Mensaje
        self.title_label = ctk.CTkLabel(self, text="📊 GENERACIÓN DE REPORTES", 
                                        font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="ew")

        self.message_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14), text_color="yellow")
        self.message_label.grid(row=1, column=0, pady=5, padx=20, sticky="ew")

        # Frame principal con filtros y resultados
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # 1. Panel de Control y Filtros
        control_frame = ctk.CTkFrame(main_frame, fg_color="#2e2e2e")
        control_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10), padx=0)
        
        # Selector de Reporte
        ctk.CTkLabel(control_frame, text="Reporte:", anchor="w").grid(row=0, column=0, padx=(10, 5), pady=6, sticky="w")
        self.reporte_combo = ctk.CTkComboBox(control_frame, 
                                            variable=self.reporte_key_var, 
                                            values=["Cargando..."],
                                            height=35, width=250)
        self.reporte_combo.grid(row=0, column=1, padx=5, pady=6, sticky="ew")

        # Expediente a filtrar
        ctk.CTkLabel(control_frame, text="Expediente:", anchor="w").grid(row=0, column=2, padx=(15, 5), pady=6, sticky="w")
        self.filtro_exp_combo = ctk.CTkComboBox(control_frame, 
                                                variable=self.filtro_exp_var, 
                                                values=["Todos", "Cargando..."],
                                                height=35, width=200)
        self.filtro_exp_combo.grid(row=0, column=3, padx=5, pady=6, sticky="ew")

        # Fecha Desde
        ctk.CTkLabel(control_frame, text="Desde:", anchor="w").grid(row=1, column=0, padx=(10, 5), pady=6, sticky="w")
        ctk.CTkEntry(control_frame, textvariable=self.filtro_desde_var, placeholder_text="YYYY-MM-DD", height=35).grid(row=1, column=1, padx=5, pady=6, sticky="ew")

        # Fecha Hasta
        ctk.CTkLabel(control_frame, text="Hasta:", anchor="w").grid(row=1, column=2, padx=(15, 5), pady=6, sticky="w")
        ctk.CTkEntry(control_frame, textvariable=self.filtro_hasta_var, placeholder_text=datetime.date.today().strftime("%Y-%m-%d"), height=35).grid(row=1, column=3, padx=5, pady=6, sticky="ew")
        
        # Botones de Acción
        btn_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        btn_frame.grid(row=0, column=4, rowspan=2, padx=10, pady=5, sticky="nsew")
        btn_frame.columnconfigure((0, 1), weight=1)

        ctk.CTkButton(btn_frame, text="⚙️ Generar", command=self._handle_generar_reporte, 
                      fg_color="#3498db", hover_color="#2980b9", height=35, 
                      font=ctk.CTkFont(size=15, weight="bold")).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
                      
        self.btn_exportar = ctk.CTkButton(btn_frame, text="⬇️ Exportar CSV/Excel", command=self._handle_exportar_reporte, 
                                          fg_color="#2ecc71", hover_color="#27ae60", height=35, 
                                          font=ctk.CTkFont(size=15, weight="bold"), state="disabled")
        self.btn_exportar.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # 2. Área de Resultados (Gráfico o Tabla)
        self.resultados_tabview = ctk.CTkTabview(main_frame, fg_color="#3c3c3c")
        self.resultados_tabview.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        
        self.resultados_tabview.add("📊 Gráfico")
        self.resultados_tabview.add("📄 Tabla de Datos")
        
        self.chart_frame = ctk.CTkFrame(self.resultados_tabview.tab("📊 Gráfico"), fg_color="#3c3c3c")
        self.chart_frame.pack(fill="both", expand=True)

        self.table_frame = ctk.CTkScrollableFrame(self.resultados_tabview.tab("📄 Tabla de Datos"), fg_color="#2e2e2e")
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.table_frame.columnconfigure(0, weight=1)

        # 3. Panel de Estadísticas
        self.stats_frame = ctk.CTkFrame(main_frame, fg_color="#2e2e2e")
        self.stats_frame.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        self.stats_labels: Dict[str, ctk.CTkLabel] = {}
        
        # Inicializar labels de estadísticas (se actualizarán con _update_stats)
        self._initialize_stats_widgets(self.stats_frame)


    def _initialize_stats_widgets(self, master_frame: ctk.CTkFrame):
        """Inicializa los widgets estáticos para mostrar estadísticas clave."""
        
        ctk.CTkLabel(master_frame, text="Estadísticas Clave", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 5))
        
        stats_data = [
            ("Total de NNA:", "total_nna", "#3498db"),
            ("Alertas Activas:", "alertas_activas", "#e74c3c"),
            ("Última Actualización:", "fecha_actualizacion", "#2ecc71"),
        ]
        
        # Frame para las estadísticas en línea
        stat_line_frame = ctk.CTkFrame(master_frame, fg_color="transparent")
        stat_line_frame.pack(fill="x", padx=20, pady=10)
        
        for i, (label_text, key, color) in enumerate(stats_data):
            # Contenedor para cada stat
            stat_container = ctk.CTkFrame(stat_line_frame, fg_color="#3c3c3c", corner_radius=8)
            stat_container.pack(side="left", fill="x", expand=True, padx=10)
            stat_container.columnconfigure(1, weight=1)

            ctk.CTkLabel(stat_container, text=label_text, font=("Arial", 13, "bold"), text_color=color).grid(row=0, column=0, padx=(10, 5), pady=10, sticky="w")
            
            # Label que contiene el valor (será actualizado)
            value_label = ctk.CTkLabel(stat_container, text="...", font=("Arial", 13), anchor="e")
            value_label.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="e")
            self.stats_labels[key] = value_label

    # ----------------------------------------------------------------------
    # Métodos de Eventos (Delegación al Controlador)
    # ----------------------------------------------------------------------

    def _handle_generar_reporte(self):
        """Recoge los filtros y llama al controlador para generar el reporte."""
        reporte_key = self.reporte_key_var.get()
        exp_str = self.filtro_exp_var.get()
        
        if reporte_key == "Seleccionar Reporte":
            self.display_message("❌ Debe seleccionar un Reporte.", is_success=False)
            return

        # LLAMADA AL NUEVO MÉTODO AÑADIDO EN EL MOCK
        exp_id = self.controller.get_expediente_id_from_str(exp_str) 

        filtros = {
            'reporte_key': reporte_key,
            'expediente_id': exp_id,
            'desde': self.filtro_desde_var.get().strip() or None,
            'hasta': self.filtro_hasta_var.get().strip() or None
        }
        
        self.controller.handle_generar_reporte(reporte_key, filtros)

    def _handle_exportar_reporte(self):
        """Llama al controlador para exportar el último reporte generado."""
        if self.last_report_data:
            # Pasa los datos y las columnas al controlador para que él maneje la exportación
            self.controller.handle_exportar_reporte(self.last_report_data, self.last_report_columns)
        else:
            self.display_message("❌ Primero genere un reporte para poder exportarlo.", is_success=False)

    # ----------------------------------------------------------------------
    # Métodos de Mutación de Vista (Llamados por el Controlador)
    # ----------------------------------------------------------------------
    
    def _cargar_reportes_disponibles(self, reportes: Dict[str, str]):
        """Carga los reportes disponibles en el ComboBox de Reportes."""
        self.reportes_map = reportes # Mantiene el mapeo de clave -> nombre
        opciones = list(reportes.values())
        if opciones:
            self.reporte_combo.configure(values=opciones)
            self.reporte_key_var.set(opciones[0])
            
    def _cargar_opciones_filtros(self, expedientes: List[Dict[str, Any]]):
        """Carga las opciones disponibles de expedientes en el filtro."""
        opciones = ["Todos"] + [exp['descripcion'] for exp in expedientes]
        self.filtro_exp_combo.configure(values=opciones)
        self.filtro_exp_var.set("Todos") 

    def display_stats(self, stats: Dict[str, Any]):
        """Actualiza el panel de estadísticas con nuevos valores."""
        for key, value in stats.items():
            if key in self.stats_labels:
                self.stats_labels[key].configure(text=str(value))

    def _limpiar_resultados(self):
        """Limpia el área de resultados (tabla y gráfico)."""
        # Limpiar Gráfico
        if self.canvas_widget:
            # Matplotlib widgets must be destroyed to free up resources
            if hasattr(self.canvas_widget, 'get_tk_widget'):
                self.canvas_widget.get_tk_widget().destroy()
            else:
                self.canvas_widget.destroy()
            self.canvas_widget = None
        
        # Limpiar Tabla
        for w in self.table_frame.winfo_children():
            w.destroy()
            
        self.last_report_data = []
        self.last_report_columns = []
        self.btn_exportar.configure(state="disabled")

    def display_results(self, data: List[Dict[str, Any]], columns: List[str], message: str):
        """Método unificado para que el controlador muestre resultados."""
        # En el mock, este método se usa para actualizar el mensaje después del gráfico.
        # En una implementación real, podría ser más robusto.
        if not data and not columns:
             # Caso de gráfico, solo mostramos el mensaje
            self.display_message(message, True)
        else:
            # Caso tabular
            self._mostrar_resultados_tabla(data, columns, message)


    def _mostrar_resultados_tabla(self, data: List[Dict[str, Any]], columnas: List[str], message: str):
        """Muestra los resultados en formato de tabla usando CTkScrollableFrame."""
        
        self._limpiar_resultados()
        self.display_message(message, True)
        self.resultados_tabview.set("📄 Tabla de Datos")
        
        if not data:
            ctk.CTkLabel(self.table_frame, text="No se encontraron datos para los filtros aplicados.", 
                         font=("Arial", 14)).pack(pady=20)
            return

        self.last_report_data = data
        self.last_report_columns = columnas
        self.btn_exportar.configure(state="normal")

        # Configuración de estilo de la tabla (usando etiquetas para simular Treeview)
        # 1. Cabecera (Header)
        header_frame = ctk.CTkFrame(self.table_frame, fg_color="#34495e")
        header_frame.pack(fill="x", padx=5, pady=(5, 0))
        header_frame.columnconfigure(tuple(range(len(columnas))), weight=1)

        for j, col in enumerate(columnas):
            ctk.CTkLabel(header_frame, text=col, font=("Arial", 13, "bold"), text_color="white", 
                         padx=10, pady=8).grid(row=0, column=j, sticky="ew")

        # 2. Filas de Datos
        for i, row_data in enumerate(data):
            row_frame = ctk.CTkFrame(self.table_frame, fg_color="#2c3e50" if i % 2 == 0 else "#3c3c3c")
            row_frame.pack(fill="x", padx=5, pady=0)
            row_frame.columnconfigure(tuple(range(len(columnas))), weight=1)
            
            for j, col in enumerate(columnas):
                value = str(row_data.get(col, ''))
                ctk.CTkLabel(row_frame, text=value, font=("Arial", 12), text_color="white", 
                             padx=10, pady=5).grid(row=0, column=j, sticky="ew")


    def _plot_chart(self, chart_type: str, data: Dict[str, float]):
        """Dibuja un gráfico de barras o circular en el frame de resultados."""
        
        if not CAN_PLOT:
            self.display_message("❌ Error: Las librerías 'pandas' y 'matplotlib' son necesarias para gráficos.", False)
            return
            
        self._limpiar_resultados()
        self.resultados_tabview.set("📊 Gráfico")

        # 1. Configurar figura y ejes
        fig, ax = plt.subplots(figsize=(6, 4))
        
        if chart_type == "bar_genero":
            labels = list(data.keys())
            values = list(data.values())
            
            colors = ['#3498db', '#e74c3c', '#9b59b6']
            
            ax.bar(labels, values, color=colors[:len(labels)])
            ax.set_title('Conteo de NNA por Género', color='white')
            ax.set_ylabel('Número de NNA', color='white')
            
            # Estilo de Matplotlib para dark mode
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            
            # Etiquetas de datos
            for i, v in enumerate(values):
                ax.text(i, v + 0.5, str(v), color='white', ha='center', fontweight='bold')
                
        # Estilo de fondo para customtkinter
        fig.patch.set_facecolor('#3c3c3c')
        ax.set_facecolor('#2e2e2e')
        plt.tight_layout()

        # 3. Integrar Matplotlib con Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        
        # Un gráfico no genera datos tabulares para exportar directamente.
        self.btn_exportar.configure(state="disabled")

    def display_message(self, message: str, is_success: bool = True):
        """Muestra un mensaje de estado en la interfaz."""
        color = "#2ecc71" if is_success else "#e74c3c"
        self.message_label.configure(text=message, text_color=color)