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
    # CORRECCIÓN: Subir solo un nivel para alcanzar la raíz del proyecto
    # (asumiendo que views/ y controllers/ están en el mismo nivel, bajo project_root)
    project_root = os.path.dirname(current_dir) 
    
    if project_root not in sys.path:
        sys.path.append(project_root)
    
    # Asegurar que el directorio actual (donde están las views) esté en el path
    views_dir = current_dir
    if os.path.exists(views_dir) and views_dir not in sys.path:
        sys.path.append(views_dir)
        
    print(f"Directorio actual (views): {current_dir}")
    print(f"Raíz del proyecto añadida a sys.path: {project_root}")
    
except NameError:
    # Este bloque se mantiene para entornos donde __file__ no está definido
    pass

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ----------------------------------------------------------------------
# MAPPING DE VISTAS (CORRECCIÓN DE RUTAS DE CONTROLADOR)
# ----------------------------------------------------------------------

MODULE_PATHS = {
    # NNA
    "gestion_nna": {
        "view_module": "funcion_vista_nna",          
        "view_class": "NNAViewFrame",                 
        "controller_module": "controllers.nna_controller",      # ✅ CLAVE Y RUTA CORRECTA
        "controller_class": "NNAControlador"          
    },
    
    # Familiares
    "gestion_familiares": {
        "view_module": "funcion_vista_fami", 
        "view_class": "FamiliarViewFrame",            
        "controller_module": "controllers.familiar_controller", # ✅ CLAVE Y RUTA CORRECTA
        "controller_class": "FamiliarControlador"        
    },
    
    # UE (Unidad de Ejecución/Entidad)
    "gestion_ue": {
        "view_module": "funcion_vista_ue", 
        "view_class": "UnidadEducativaViewFrame",        
        "controller_module": "controllers.unidad_educativa_controller", # ✅ CLAVE Y RUTA CORRECTA
        "controller_class": "UnidadEducativaControlador" 
    },
    
    # Matrículas
    "gestion_matriculas": {
        "view_module": "funcion_vista_matricula", 
        "view_class": "MatriculaViewFrame",             
        "controller_module": "controllers.matricula_controller", # ✅ CLAVE Y RUTA CORRECTA
        "controller_class": "MatriculaControlador"       
    },
    
    # Artículos
    "gestion_articulos": {
        "view_module": "funcion_vista_art",
        "view_class": "ArticuloViewFrame",             
        "controller_module": "controllers.articulo_controller", # ✅ CLAVE Y RUTA CORRECTA
        "controller_class": "ArticuloControlador"       
    },
    
    # Personal
    "gestion_personal": {
        "view_module": "funcion_vista_personal", 
        "view_class": "PersonalViewFrame",             
        "controller_module": "controllers.personal_controller", # ✅ CLAVE Y RUTA CORRECTA
        "controller_class": "PersonalControlador"        
    },
    
    # Configuración
    "configuracion": {
        "view_module": "configuracion_view",
        "view_class": "ConfiguracionViewFrame",         
        "controller_module": "controllers.configuracion_controller", # ✅ CLAVE Y RUTA CORRECTA
        "controller_class": "ConfiguracionControlador"   
    },
    
    # Reportes
    "reportes": {
        "view_module": "reportes_view", 
        "view_class": "ReportesViewFrame",                  
        "controller_module": "controllers.reportes_controller", # ✅ CLAVE Y RUTA CORRECTA
        "controller_class": "ReportesControlador"      
    }, 
    
    # Seguimiento de Expedientes
    "seguimiento_expedientes": {
        "view_module": "funcion_vista_seguimiento_expedientes", 
        "view_class": "SeguimientoExpedienteViewFrame", 
        "controller_module": "controllers.seguimiento_expediente_controllers", # ✅ CLAVE Y RUTA CORRECTA
        "controller_class": "SeguimientoExpedienteControlador"     
    }, 
}

class BaseViewFrame(ctk.CTkFrame):
    """Clase base para módulos de vista que asegura la configuración de grid."""
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller 
        self.pack_propagate(False) 
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
    def __init__(self, role=None):
        super().__init__()
        self.role = role # Almacenar el rol
        self.title(f"🏛️ Sistema de Gestión LOPNNA - Consejo de Protección Carrizal ({role if role else 'Invitado'})") 
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
        """Helper para extraer la información de configuración del módulo."""
        return MODULE_PATHS.get(module_name, {})


    def show_view(self, module_name):
        """Carga y muestra la vista, manejando controladores para módulos MVC completos."""
        
        # 1. Manejar Inicio
        if module_name == "menu_inicio":
            if module_name not in self._frames:
                frame = MenuInicioFrame(self.main_content_frame, self)
                self._frames[module_name] = frame
        
        # Ocultar todos los frames
        for frame_item in self._frames.values():
            frame_item.grid_forget()
        
        if module_name not in self._frames:
            # Intento de carga de la vista (Instanciación)
            try:
                # Obtener la información completa (usando las 4 claves)
                info = self._get_module_info(module_name)
                
                view_module_path = info.get('view_module') 
                view_class_name = info.get('view_class') 
                controller_module_path = info.get('controller_module')
                controller_class_name = info.get('controller_class') 
                
                if not view_module_path or not view_class_name:
                    # Resuelve el error "Falta 'view_module' o 'view_class'"
                    raise ValueError(f"Falta 'view_module' o 'view_class' en la configuración de {module_name}.")

                # 1. Cargar el Módulo de la Vista
                # Nota: Si el view_module también está en la carpeta 'views', funcionará
                # gracias a que 'views_dir' se añadió a sys.path.
                view_module = importlib.import_module(view_module_path) 
                ViewClass = getattr(view_module, view_class_name)

                if controller_module_path and controller_class_name:
                    # 🔴 MÓDULO MVC COMPLETO (Controlador Externo)
                    
                    # 2. Cargar el Módulo del Controlador
                    # Aquí se usa la ruta completa: 'controllers.nna_controller'
                    controller_module = importlib.import_module(controller_module_path)
                    ControllerClass = getattr(controller_module, controller_class_name)

                    # 3. Instanciar el Controlador (solo una vez)
                    if module_name not in self._controllers:
                        controller_instance = ControllerClass()
                        self._controllers[module_name] = controller_instance 
                    
                    controller_instance = self._controllers[module_name]
                    
                    # 4. Instanciar la Vista, pasándole el Controlador Real
                    frame = ViewClass(self.main_content_frame, controller_instance)
                    
                else:
                    # 🟢 MÓDULO SIMPLE (MenuApp actúa como Controlador)
                    frame = ViewClass(self.main_content_frame, self) 
                    
                
                # Almacenar la vista instanciada en el caché
                self._frames[module_name] = frame
                frame.grid(row=0, column=0, sticky="nsew")

            except ImportError as e:
                # Si falla, es porque la ruta del controlador (controllers.nombre_modulo) no se resolvió
                msg_error = f"No se pudo importar el módulo: {module_name}. Verifique que el archivo del Controlador ({controller_module_path}.py) exista en la carpeta 'controllers/' dentro de la raíz del proyecto.\nError detallado: {e}"
                messagebox.showerror("❌ Error de Importación", msg_error)
                print(f"Error de Importación del módulo {module_name}: {e}")
                return 
            except Exception as e:
                msg_error = f"Error al instanciar la clase {view_class_name} del módulo {module_name}.\nVerifique el constructor de la vista y que la clase exista.\nError: {e}"
                messagebox.showerror("❌ Error de Carga de Vista", msg_error)
                print(f"Error al instanciar la vista {module_name}: {e}")
                return 
        
        # Mostrar solo el frame deseado
        current_frame = self._frames[module_name]
        current_frame.grid(row=0, column=0, sticky="nsew")
        
        # Llamar al método show.
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

def main(role=None): 
    try:
        print("Iniciando aplicación en modo panel lateral...")
        app = MenuApp(role=role) 
        app.mainloop()
        print("El sistema ha sido cerrado correctamente.")
        
    except Exception as e:
        messagebox.showerror("❌ Error Crítico", f"No se pudo iniciar el sistema: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()