# views/reportes_view.py
import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import List, Dict

class ReportesView:
    """
    Vista para el módulo de reportes del sistema NNA
    """
    
    def __init__(self, root):
        self.root = root
        self.controlador = None
        
        # Configuración de temas
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        self.crear_interfaz()
    
    def set_controlador(self, controlador):
        """Establece el controlador para esta vista"""
        self.controlador = controlador
    
    def crear_interfaz(self):
        """Crea la interfaz gráfica principal"""
        self.root.title("Módulo de Reportes - Sistema de Protección NNA")
        self.root.geometry("1000x700")
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Módulo de Reportes y Gestión NNA", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Crear pestañas
        self.crear_pestana_gestion_nna()
        self.crear_pestana_reportes_nna()
        self.crear_pestana_reportes_familiares()
        self.crear_pestana_reportes_denuncias()
        self.crear_pestana_estadisticas()
    
    def crear_pestana_gestion_nna(self):
        """Crea la pestaña de gestión de NNA"""
        frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(frame, text="Gestión NNA")
        
        # Frame de formulario de ingreso
        self.crear_formulario_ingreso_datos(frame)
        
        # Frame de botones de acción
        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(
            btn_frame, 
            text="Cargar NNA", 
            command=self.cargar_nna
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame, 
            text="Exportar Excel", 
            command=lambda: self.exportar_datos("nna")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame, 
            text="Exportar PDF", 
            command=lambda: self.exportar_pdf("nna")
        ).pack(side="left", padx=5)
        
        # Tabla para mostrar NNA
        self.crear_tabla_nna(frame)
    
    def crear_formulario_ingreso_datos(self, parent_frame):
        """Crea un formulario para ingresar datos de prueba"""
        form_frame = ctk.CTkFrame(parent_frame)
        form_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            form_frame, 
            text="Ingresar Datos de Prueba", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=5)
        
        # Campos del formulario
        campos_frame = ctk.CTkFrame(form_frame)
        campos_frame.pack(fill="x", pady=10)
        
        # Función de validación para solo letras y espacios
        def validar_solo_letras(texto):
            """Valida que el texto contenga solo letras y espacios"""
            if texto == "":
                return True
            # Permite letras, espacios, y algunos caracteres especiales comunes en nombres
            return all(c.isalpha() or c.isspace() or c in "áéíóúÁÉÍÓÚñÑ" for c in texto)
        # Registrar la función de validación
        vcmd = (self.root.register(validar_solo_letras), '%P')
        
        # Nombre
        ctk.CTkLabel(campos_frame, text="Primer Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nombre = ctk.CTkEntry(
            campos_frame, 
            width=150,
            validate="key",
            validatecommand=vcmd
            )
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)
        
        # Apellido
        ctk.CTkLabel(campos_frame, text="Primer Apellido:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_apellido = ctk.CTkEntry(
            campos_frame, 
            width=150,
            validate="key",
            validatecommand=vcmd
            )
        self.entry_apellido.grid(row=0, column=3, padx=5, pady=5)
        
        # Edad (solo números)
        def validar_solo_numeros(texto):
            """Valida que el texto contenga solo números"""
            if texto == "":
                return True
            return texto.isdigit()
    
        vcmd_numeros = (self.root.register(validar_solo_numeros), '%P')
    
        ctk.CTkLabel(campos_frame, text="Edad:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_edad = ctk.CTkEntry(
            campos_frame, 
            width=150,
            validate="key",
            validatecommand=vcmd_numeros
            )
        self.entry_edad.grid(row=1, column=1, padx=5, pady=5)
    
        # Género
        ctk.CTkLabel(campos_frame, text="Género:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.combo_genero = ctk.CTkComboBox(campos_frame, values=["M", "F"], width=150)
        self.combo_genero.grid(row=1, column=3, padx=5, pady=5)
        self.combo_genero.set("M")
        
        # Teléfono (solo números y algunos caracteres especiales)
        def validar_telefono(texto):
            """Valida que el texto sea un teléfono válido"""
            if texto == "":
                return True
            # Permite números, espacios, paréntesis, guiones y +
            return all(c.isdigit() or c in " +-()" for c in texto)
    
        vcmd_telefono = (self.root.register(validar_telefono), '%P')
    
        ctk.CTkLabel(campos_frame, text="Teléfono:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_telefono = ctk.CTkEntry(
            campos_frame, 
            width=150,
            validate="key",
            validatecommand=vcmd_telefono
            )
        self.entry_telefono.grid(row=2, column=1, padx=5, pady=5)
        
        # Dirección
        ctk.CTkLabel(campos_frame, text="Dirección:").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.entry_direccion = ctk.CTkEntry(campos_frame, width=150)
        self.entry_direccion.grid(row=2, column=3, padx=5, pady=5)
        
        # Botones
        botones_frame = ctk.CTkFrame(form_frame)
        botones_frame.pack(fill="x", pady=10)
        
        ctk.CTkButton(
            botones_frame, 
            text="Agregar NNA", 
            command=self.agregar_nna
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            botones_frame, 
            text="Generar Datos de Prueba", 
            command=self.generar_datos_prueba
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            botones_frame, 
            text="Limpiar Formulario", 
            command=self.limpiar_formulario
        ).pack(side="left", padx=5)
        
        # Tooltip informativo
        info_label = ctk.CTkLabel(
            form_frame, 
            text="ℹ️ Los campos de nombre y apellido solo aceptan letras",
            text_color="gray",
            font=ctk.CTkFont(size=12)
            )
        info_label.pack(pady=5)

    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.entry_nombre.delete(0, "end")
        self.entry_apellido.delete(0, "end")
        self.entry_edad.delete(0, "end")
        self.entry_telefono.delete(0, "end")
        self.entry_direccion.delete(0, "end")
        self.combo_genero.set("M")
    
    def crear_tabla_nna(self, parent_frame):
        """Crea la tabla para mostrar NNA"""
        table_frame = ctk.CTkFrame(parent_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbar
        scroll_y = ttk.Scrollbar(table_frame)
        scroll_y.pack(side="right", fill="y")
        
        scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")
        
        # Treeview
        self.tree_nna = ttk.Treeview(
            table_frame,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )
        
        scroll_y.configure(command=self.tree_nna.yview)
        scroll_x.configure(command=self.tree_nna.xview)
        
        # Configurar columnas
        columnas = [
            "ID", "Documento", "Nombre", "Apellido", "Género", 
            "Edad", "Teléfono", "Dirección"
        ]
        self.tree_nna["columns"] = columnas
        self.tree_nna["show"] = "headings"
        
        for col in columnas:
            self.tree_nna.heading(col, text=col)
            self.tree_nna.column(col, width=100)
        
        self.tree_nna.pack(fill="both", expand=True)
    
    def crear_pestana_reportes_nna(self):
        """Crea la pestaña de reportes de NNA"""
        frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(frame, text="Reportes NNA")
        
        self.crear_frame_reportes(frame, "NNA", "nna")
    
    def crear_pestana_reportes_familiares(self):
        """Crea la pestaña de reportes familiares"""
        frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(frame, text="Reportes Familiares")
        
        self.crear_frame_reportes(frame, "Familiares", "familiares")
    
    def crear_pestana_reportes_denuncias(self):
        """Crea la pestaña de reportes de denuncias"""
        frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(frame, text="Reportes Denuncias")
        
        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(
            btn_frame, 
            text="Cargar Denuncias", 
            command=self.cargar_denuncias
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame, 
            text="Cargar Expedientes", 
            command=self.cargar_expedientes
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame, 
            text="Exportar Excel", 
            command=lambda: self.exportar_datos("denuncias")
        ).pack(side="left", padx=5)
        
        # Tabla para denuncias/expedientes
        self.crear_tabla_generica(frame)
    
    def crear_pestana_estadisticas(self):
        """Crea la pestaña de estadísticas"""
        frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(frame, text="Estadísticas")
        
        # Botones de estadísticas
        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(
            btn_frame, 
            text="NNA por Género", 
            command=self.mostrar_estadistica_genero
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame, 
            text="Denuncias por Estado", 
            command=self.mostrar_estadistica_denuncias
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame, 
            text="NNA por Edad", 
            command=self.mostrar_estadistica_edad
        ).pack(side="left", padx=5)
        
        # Frame para gráficos
        self.stats_frame = ctk.CTkFrame(frame)
        self.stats_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    def crear_frame_reportes(self, parent_frame, titulo: str, tipo: str):
        """Crea un frame genérico para reportes"""
        btn_frame = ctk.CTkFrame(parent_frame)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(
            btn_frame, 
            text=f"Cargar {titulo}", 
            command=lambda: self.cargar_datos_tipo(tipo)
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame, 
            text="Exportar Excel", 
            command=lambda: self.exportar_datos(tipo)
        ).pack(side="left", padx=5)
        
        # Tabla genérica
        self.crear_tabla_generica(parent_frame)
    
    def crear_tabla_generica(self, parent_frame):
        """Crea una tabla genérica para mostrar datos"""
        table_frame = ctk.CTkFrame(parent_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(table_frame)
        scroll_y.pack(side="right", fill="y")
        
        scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")
        
        # Treeview
        self.tree_generico = ttk.Treeview(
            table_frame,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )
        
        scroll_y.configure(command=self.tree_generico.yview)
        scroll_x.configure(command=self.tree_generico.xview)
        
        self.tree_generico.pack(fill="both", expand=True)
    
    def configurar_columnas_tabla(self, treeview, columnas: List[str]):
        """Configura las columnas de una tabla"""
        treeview["columns"] = columnas
        treeview["show"] = "headings"
        
        for col in columnas:
            treeview.heading(col, text=col)
            treeview.column(col, width=120)
    
    def limpiar_tabla(self, treeview):
        """Limpia todos los elementos de una tabla"""
        for item in treeview.get_children():
            treeview.delete(item)
    
    def mostrar_datos_tabla(self, treeview, datos: List[Dict], columnas: List[str]):
        """Muestra datos en una tabla"""
        self.limpiar_tabla(treeview)
        self.configurar_columnas_tabla(treeview, columnas)
        
        for fila in datos:
            valores = [str(fila.get(col, "")) for col in columnas]
            treeview.insert("", "end", values=valores)
    
    def mostrar_grafico(self, datos: List[Dict], titulo: str, tipo: str = "pie"):
        """Muestra un gráfico en el frame de estadísticas"""
        # Limpiar frame anterior
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        if not datos:
            ctk.CTkLabel(
                self.stats_frame, 
                text="No hay datos para mostrar"
            ).pack(expand=True)
            return
        
        fig, ax = plt.subplots(figsize=(8, 6), facecolor='lightgray')
        
        if tipo == "pie":
            labels = [f"{item[list(item.keys())[0]]} ({item['total']})" for item in datos]
            sizes = [item['total'] for item in datos]
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        elif tipo == "bar":
            categorias = [item[list(item.keys())[0]] for item in datos]
            valores = [item['total'] for item in datos]
            ax.bar(categorias, valores, color='gray')
            ax.set_xlabel("Categorías")
            ax.set_ylabel("Total")
        
        ax.set_title(titulo, color='black')
        
        canvas = FigureCanvasTkAgg(fig, master=self.stats_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)
    
    def mostrar_mensaje(self, titulo: str, mensaje: str, tipo: str = "info"):
        """
        Muestra un mensaje al usuario usando tkinter.messagebox estándar
        """
        try:
            if tipo == "error":
                messagebox.showerror(titulo, mensaje)
            elif tipo == "warning":
                messagebox.showwarning(titulo, mensaje)
            else:  # info o éxito
                messagebox.showinfo(titulo, mensaje)
        except Exception as e:
            # Fallback en caso de error
            print(f"[ERROR] No se pudo mostrar mensaje: {e}")
    
    def obtener_datos_formulario_nna(self) -> Dict[str, str]:
        """Obtiene los datos del formulario de NNA
            Returns: Dict: Datos del formulario"""
        return {
            'nombre': self.entry_nombre.get().strip(),
            'apellido': self.entry_apellido.get().strip(),
            'edad': self.entry_edad.get().strip(),
            'genero': self.combo_genero.get(),
            'telefono': self.entry_telefono.get().strip(),
            'direccion': self.entry_direccion.get().strip()
            }
    
    def actualizar_lista_nna(self):
        """Actualiza la tabla de NNA con los datos actuales del controlador"""
        if self.controlador:
            try:
                datos_nna = self.controlador.obtener_datos_por_tipo("nna")
                if datos_nna:
                    columnas = list(datos_nna[0].keys())
                    self.mostrar_datos_tabla(self.tree_nna, datos_nna, columnas)
                else:
                    self.limpiar_tabla(self.tree_nna)
            except Exception as e:
                print(f"[ERROR] Error actualizando lista NNA: {e}")

            
    def actualizar_vista_datos(self):
        """Actualiza todas las vistas de datos"""
        
        if self.controlador:
            try:
                datos_nna = self.controlador.obtener_datos_por_tipo("nna")
                if datos_nna:
                    columnas = list(datos_nna[0].keys())
                    self.mostrar_datos_tabla(self.tree_nna, datos_nna, columnas)
                else:
                    self.limpiar_tabla(self.tree_nna)
            except Exception as e:
                print(f"[ERROR] Error actualizando vista: {e}")
            
    # ========== MÉTODOS DE CALLBACK ==========
    
    def cargar_nna(self):
        if self.controlador:
            self.controlador.cargar_nna()
    
    def cargar_denuncias(self):
        if self.controlador:
            self.controlador.cargar_denuncias()
    
    def cargar_expedientes(self):
        if self.controlador:
            self.controlador.cargar_expedientes()
    
    def cargar_datos_tipo(self, tipo: str):
        if self.controlador:
            self.controlador.cargar_datos_tipo(tipo)
    
    def exportar_datos(self, tipo: str):
        if self.controlador:
            self.controlador.exportar_datos(tipo)
    
    def exportar_pdf(self, tipo: str):
        if self.controlador:
            self.controlador.exportar_pdf(tipo)
    
    def mostrar_estadistica_genero(self):
        if self.controlador:
            self.controlador.mostrar_estadistica_genero()
    
    def mostrar_estadistica_denuncias(self):
        if self.controlador:
            self.controlador.mostrar_estadistica_denuncias()
    
    def mostrar_estadistica_edad(self):
        if self.controlador:
            self.controlador.mostrar_estadistica_edad()
    
    def agregar_nna(self):
        """Agrega un nuevo NNA desde el formulario"""
        if self.controlador:
            datos_nna = self.obtener_datos_formulario_nna()
            # Validación adicional
            if not datos_nna['nombre'] or not datos_nna['apellido']:
                self.mostrar_mensaje("Error", "Nombre y apellido son requeridos", "error")
                return
            # Validar que nombre y apellido contengan solo letras
            def contiene_solo_letras(texto):
                return all(c.isalpha() or c.isspace() or c in "áéíóúÁÉÍÓÚñÑ" for c in texto)
            
            if not contiene_solo_letras(datos_nna['nombre']):
                self.mostrar_mensaje("Error", "El nombre solo puede contener letras", "error")
                self.entry_nombre.focus()
                return
            if not contiene_solo_letras(datos_nna['apellido']):
                self.mostrar_mensaje("Error", "El apellido solo puede contener letras", "error")
                self.entry_apellido.focus()
                return
            
            if datos_nna['edad']:
                if not datos_nna['edad'].isdigit():
                    self.mostrar_mensaje("Error", "La edad debe ser un número", "error")
                    self.entry_edad.focus()
                    return
                edad = int(datos_nna['edad'])
                if edad < 0 or edad > 120:
                    self.mostrar_mensaje("Error", "La edad debe estar entre 0 y 120 años", "error")
                    self.entry_edad.focus()
                    return
        
            self.controlador.agregar_nna(datos_nna)
            self.limpiar_formulario()
    
    def generar_datos_prueba(self):
        if self.controlador:
            self.controlador.generar_datos_prueba()