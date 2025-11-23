import customtkinter as ctk
from tkinter import messagebox
import sys
import os
import importlib

# ----------------------------------------------------------------------
# Configuración de Paths y Apariencia
# ----------------------------------------------------------------------

# Configurar el path para importaciones
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir)) # Subir dos niveles para Proyecto_prueba
    if project_root not in sys.path:
        sys.path.append(project_root)
    
    views_dir = current_dir
    if os.path.exists(views_dir) and views_dir not in sys.path:
        sys.path.append(views_dir)
        
except NameError:
    pass

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ----------------------------------------------------------------------
# MAPPING DE VISTAS
# ----------------------------------------------------------------------

# Usamos el formato de diccionario para TODAS las vistas que usan una clase
# de vista específica (no 'ViewFrame') o para ser explícitos.

MODULE_PATHS = {
    "gestion_nna": {"module": "funcion_vista_nna", "class": "ViewFrame"},
    "gestion_familiares": {"module": "funcion_vista_fami", "class": "ViewFrame"},
    "gestion_ue": {"module": "funcion_vista_ue", "class": "ViewFrame"},
    "gestion_matriculas": {"module": "funcion_vista_matricula", "class": "ViewFrame"},
    
    # Artículos (Asumimos ArticuloVista o ViewFrame)
    "gestion_articulos": {
        "module": "funcion_vista_art",
        "class": "ArticuloVista" # <- Se usará ArticuloVista o ViewFrame si se cambia
    },
    
    "gestion_personal": {"module": "funcion_vista_personal", "class": "ViewFrame"},
    
    # Configuración (Corregido para usar el nombre de clase correcto)
    "configuracion": {
        "module": "configuracion_view",
        "class": "ConfiguracionView" # <- Basado en tu archivo configuracion_view.py
    },
    
    "reportes": {"module": "reportes_view", "class": "ViewFrame"}, 
    "seguimiento_expedientes": {"module": "seguimiento_view", "class": "ViewFrame"}, 
}

# ----------------------------------------------------------------------
# VISTA INICIAL (MenuInicioFrame)
# ----------------------------------------------------------------------

class BaseViewFrame(ctk.CTkFrame):
    """Clase base para módulos de vista que asegura la configuración de grid."""
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller 
        # CORRECCIÓN: Eliminado pack_propagate(False) ya que la app usa grid, 
        # y esta configuración puede interferir con el uso de grid.
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def show(self):
        """Método para cargar datos o actualizar la vista."""
        pass

class MenuInicioFrame(BaseViewFrame):
    """Vista de inicio simple."""
    def __init__(self, master, controller):
        super().__init__(master, controller)
        self.configure(fg_color="transparent")
        
        # Contenedor central
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(container, 
                     text="Bienvenido al Sistema de Gestión LOPNNA", 
                     font=("Arial", 36, "bold"), 
                     text_color="#f1c40f").pack(pady=10)
        
        ctk.CTkLabel(container, 
                     text="Seleccione un módulo del panel lateral para comenzar.", 
                     font=("Arial", 18)).pack(pady=10)
        
        ctk.CTkButton(container, 
                      text="Iniciar Gestión de NNA",
                      command=lambda: self.controller.show_view("gestion_nna"),
                      fg_color="#3498db",
                      hover_color="#2980b9",
                      height=50,
                      font=("Arial", 16, "bold"),
                      corner_radius=10).pack(pady=20, padx=50)


# ----------------------------------------------------------------------
# CLASE PRINCIPAL: MenuApp
# ----------------------------------------------------------------------

class MenuApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🏛️ Sistema de Gestión LOPNNA - Consejo de Protección Carrizal")
        self.geometry("1400x900")
        self.minsize(1200, 800)
        self.center_window()
        
        self._frames = {} 
        self._controllers = {}
        
        self.setup_main_layout()
        self.show_view("menu_inicio") 
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_main_layout(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0) 
        self.grid_columnconfigure(1, weight=1) 

        self.sidebar_frame = ctk.CTkFrame(self, 
                                          width=280, 
                                          corner_radius=0, 
                                          fg_color="#2c3e50")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1)
        
        ctk.CTkLabel(self.sidebar_frame, 
                     text="🏛️ SISTEMA LOPNNA", 
                     font=("Arial", 18, "bold"), 
                     text_color="#f1c40f").grid(row=0, column=0, padx=20, pady=(20, 10))
        
        ctk.CTkFrame(self.sidebar_frame, height=2, fg_color="#34495e").grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 15))

        self.main_content_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_content_frame.grid(row=0, column=1, sticky="nsew")
        self.main_content_frame.grid_rowconfigure(0, weight=1)
        self.main_content_frame.grid_columnconfigure(0, weight=1)
        
        self.create_sidebar_buttons()


    def create_sidebar_buttons(self):
        modules = [
            {"text": "Menú Inicio", "command": "menu_inicio", "emoji": "🏠"},
            {"text": "Gestión de NNA", "command": "gestion_nna", "emoji": "👦"},
            {"text": "Gestión de Familiares", "command": "gestion_familiares", "emoji": "👨‍👩‍👧‍👦"},
            {"text": "Unidades Educativas", "command": "gestion_ue", "emoji": "🏫"},
            {"text": "Gestión de Matrículas", "command": "gestion_matriculas", "emoji": "📚"},
            {"text": "Gestión de Artículos", "command": "gestion_articulos", "emoji": "📦"},
            {"text": "Gestión de Personal", "command": "gestion_personal", "emoji": "👥"},
            {"text": "Seguimiento Expedientes", "command": "seguimiento_expedientes", "emoji": "📌"},
            {"text": "Reportes y Estadísticas", "command": "reportes", "emoji": "📊"},
            {"text": "Configuración del Sistema", "command": "configuracion", "emoji": "⚙️"},
        ]
        
        for i, module in enumerate(modules):
            button = ctk.CTkButton(
                self.sidebar_frame,
                text=f"{module['emoji']} {module['text']}",
                # 🔴 CORRECCIÓN: self.show_view ahora maneja la carga y el caché.
                command=lambda cmd=module['command']: self.show_view(cmd),
                height=40,
                corner_radius=8,
                fg_color="transparent",
                hover_color="#34495e",
                font=("Arial", 14, "bold"),
                anchor="w"
            )
            button.grid(row=i + 2, column=0, padx=15, pady=5, sticky="ew")

        ctk.CTkButton(
            self.sidebar_frame,
            text="❓ Ayuda",
            command=self.mostrar_ayuda,
            height=30,
            fg_color="#f39c12",
            hover_color="#e67e22",
            font=("Arial", 12)
        ).grid(row=11, column=0, padx=20, pady=(20, 5), sticky="s")
        
        ctk.CTkButton(
            self.sidebar_frame,
            text="🚪 Salir",
            command=self.on_closing,
            height=30,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            font=("Arial", 12, "bold")
        ).grid(row=12, column=0, padx=20, pady=(5, 20), sticky="s")


    def _get_module_info(self, module_name):
        """Helper para extraer la ruta del módulo y el nombre de la clase."""
        path_info = MODULE_PATHS.get(module_name)
        
        if not path_info:
            # Maneja módulos simples que quizás no tienen un mapeo de diccionario
            return module_name, "ViewFrame"
        
        if isinstance(path_info, str):
            # Asume ViewFrame si es solo una cadena (para compatibilidad)
            return path_info, "ViewFrame"
        elif isinstance(path_info, dict):
            module_path = path_info.get('module')
            class_name = path_info.get('class')
            if not module_path or not class_name:
                 raise ValueError(f"Falta 'module' o 'class' en la configuración de {module_name}")
            return module_path, class_name
        
        raise ValueError(f"Formato de path no soportado para {module_name}")


    def show_view(self, module_name):
        """Carga y muestra la vista, o la obtiene del caché si ya está instanciada."""
        
        if module_name not in self._frames:
            # Intento de carga de la vista (Instanciación)
            frame = None
            
            try:
                if module_name == "menu_inicio":
                    frame = MenuInicioFrame(self.main_content_frame, self)
                else:
                    module_path, class_name = self._get_module_info(module_name)
                    
                    # Importación dinámica
                    # Nota: Importamos desde el directorio views/ (que está en sys.path)
                    module = importlib.import_module(module_path) 
                    ViewClass = getattr(module, class_name)
                    
                    # 🔴 CLAVE DE LA CORRECCIÓN: Pasar 'self' (la instancia de MenuApp) 
                    # como 'controller' a la vista real.
                    frame = ViewClass(self.main_content_frame, self) 
                    
                
                # Almacenar la vista instanciada en el caché
                self._frames[module_name] = frame
                frame.grid(row=0, column=0, sticky="nsew")

            except ImportError as e:
                msg = f"No se pudo importar el módulo real: {module_name} ({module_path}).\nVerifique que el archivo exista y no tenga errores.\nError: {e}"
                messagebox.showerror("❌ Error de Importación", msg)
                print(f"Error de Importación del módulo {module_name}: {e}")
                return # Salir si la carga falla
            except Exception as e:
                msg = f"Error al instanciar la clase {class_name} del módulo {module_name}.\nVerifique el constructor de la vista.\nError: {e}"
                messagebox.showerror("❌ Error de Carga de Vista", msg)
                print(f"Error al instanciar la vista {module_name}: {e}")
                return # Salir si la carga falla
        
        # Ocultar todos los frames y mostrar solo el frame deseado
        for frame_item in self._frames.values():
            frame_item.grid_forget()
            
        current_frame = self._frames[module_name]
        current_frame.grid(row=0, column=0, sticky="nsew")
        
        # Llamar al método show. En los módulos MVC, esto disparará la carga de datos.
        current_frame.show() 
        
        print(f"Vista cargada en panel lateral: {module_name}")

    def center_window(self):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 1400) // 2
        y = (screen_height - 900) // 2
        self.geometry(f'1400x900+{x}+{y}')

    def mostrar_ayuda(self):
        ayuda_texto = """
🏛️ SISTEMA DE GESTIÓN LOPNNA
Este sistema permite la administración integral de:
- Niños, Niñas y Adolescentes (NNA)
- Familiares y Representantes
- Unidades Educativas
- Matrículas, Artículos y Personal
- Seguimiento de Expedientes
- Reportes
"""
        messagebox.showinfo("❓ Ayuda del Sistema", ayuda_texto)
    
    def on_closing(self):
        if messagebox.askyesno("🚪 Salir del Sistema", "¿Está seguro de que desea salir del sistema?"):
            self.destroy()

# ----------------------------------------------------------------------
# PUNTO DE ENTRADA
# ----------------------------------------------------------------------

def main():
    try:
        print("Iniciando aplicación en modo panel lateral...")
        app = MenuApp()
        app.mainloop()
        print("El sistema ha sido cerrado correctamente.")
        
    except Exception as e:
        messagebox.showerror("❌ Error Crítico", f"No se pudo iniciar el sistema: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()