# menu.py
import customtkinter as ctk
from tkinter import messagebox
import sys
import os

# Configurar el path para importaciones
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuración de apariencia
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MenuApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🏛️ Sistema de Gestión LOPNNA - Consejo de Protección Carrizal")
        
        # Configurar para pantalla grande
        self.attributes('-fullscreen', False)
        self.geometry("1400x900")
        self.minsize(1200, 800)
        
        # Centrar ventana
        self.center_window()
        
        # Configurar layout principal
        self.setup_main_layout()
        
        # Manejar cierre de ventana
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_main_layout(self):
        """Configurar el layout principal del menú"""
        # Frame principal
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Header con información
        header_frame = ctk.CTkFrame(main_container, height=100)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)

        # Contenido del header
        title_label = ctk.CTkLabel(
            header_frame,
            text="🏛️ SISTEMA DE GESTIÓN LOPNNA",
            font=("Arial", 28, "bold"),
            text_color="#2e86ab"
        )
        title_label.pack(pady=10)

        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Consejo de Protección de Niños, Niñas y Adolescentes - Municipio Carrizal",
            font=("Arial", 16),
            text_color="#7f8c8d"
        )
        subtitle_label.pack()
        
        # Definir módulos con emojis y colores
        modules = [
            # ... (Módulos existentes: Gestión de NNA, Gestión de Familiares, Unidades Educativas, Gestión de Matrículas, Gestión de Artículos, Gestión de Personal)
            {
                "emoji": "👦", "text": "Gestión de NNA", 
                "command": self.gestion_nna, "color": "#3498db",
                "description": "Administrar información de\nNiños, Niñas y Adolescentes"
            },
            {
                "emoji": "👨‍👩‍👧‍👦", "text": "Gestión de Familiares", 
                "command": self.gestion_familiares, "color": "#9b59b6",
                "description": "Gestionar datos de\nfamiliares y tutores"
            },
            {
                "emoji": "🏫", "text": "Unidades Educativas", 
                "command": self.gestion_ue, "color": "#e74c3c",
                "description": "Administrar Unidades\nEducativas"
            },
            {
                "emoji": "📚", "text": "Gestión de Matrículas", 
                "command": self.gestion_matriculas, "color": "#f39c12",
                "description": "Controlar matrículas\neducativas"
            },
            {
                "emoji": "📦", "text": "Gestión de Artículos", 
                "command": self.gestion_articulos, "color": "#1abc9c",
                "description": "Administrar artículos\ndel sistema"
            },
            {
                "emoji": "👥", "text": "Gestión de Personal", 
                "command": self.gestion_personal, "color": "#34495e",
                "description": "Gestionar usuarios\ndel sistema"
            },
            # --- NUEVOS MÓDULOS ---
            {
                "emoji": "📌", "text": "Seguimiento Expedientes", 
                "command": self.seguimiento_expedientes, "color": "#2ecc71", # Verde Esmeralda
                "description": "Registrar y consultar\nel seguimiento de expedientes"
            },
            {
                "emoji": "⚙️", "text": "Configuración del Sistema", 
                "command": self.configuracion, "color": "#f1c40f", # Amarillo Girasol
                "description": "Administración de Roles\ny Usuarios"
            },
            {
                "emoji": "📊", "text": "Reportes y Estadísticas", 
                "command": self.reportes, "color": "#e67e22", # Naranja Zanahoria
                "description": "Visualizar reportes\ny datos estadísticos"
            },
            # ------------------------
        ]
        
        # Frame para los módulos
        modules_frame = ctk.CTkFrame(main_container)
        modules_frame.pack(fill="both", expand=True)

        # Título de módulos
        modules_title = ctk.CTkLabel(
            modules_frame,
            text="📋 MÓDULOS DEL SISTEMA",
            font=("Arial", 20, "bold"),
            text_color="#2e86ab"
        )
        modules_title.pack(pady=20)

        # Grid para los botones de módulos
        buttons_grid = ctk.CTkFrame(modules_frame, fg_color="transparent")
        buttons_grid.pack(fill="both", expand=True, padx=50, pady=20)

        # Configurar grid layout
        buttons_grid.columnconfigure(0, weight=1)
        buttons_grid.columnconfigure(1, weight=1)
        buttons_grid.columnconfigure(2, weight=1)
        buttons_grid.rowconfigure(0, weight=1)
        buttons_grid.rowconfigure(1, weight=1)
        buttons_grid.rowconfigure(2, weight=1)
        
        # Crear botones en grid
        for i, module in enumerate(modules):
            row = i // 3
            col = i % 3
            
            self.create_module_button(
                buttons_grid, module, row, col
            )

        # Frame para botones de control
        control_frame = ctk.CTkFrame(main_container, height=80)
        control_frame.pack(fill="x", pady=(20, 0))
        control_frame.pack_propagate(False)

        # Botones de control
        control_buttons_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        control_buttons_frame.pack(expand=True)

        # Botón de ayuda
        help_button = ctk.CTkButton(
            control_buttons_frame,
            text="❓ Ayuda del Sistema",
            command=self.mostrar_ayuda,
            height=40,
            font=("Arial", 14),
            fg_color="#f39c12",
            hover_color="#e67e22"
        )
        help_button.pack(side="left", padx=10)

        # Botón de cerrar sesión
        logout_button = ctk.CTkButton(
            control_buttons_frame,
            text="🚪 Salir del Sistema",
            command=self.on_closing,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        logout_button.pack(side="right", padx=10)

    def create_module_button(self, parent, module, row, col):
        """Crear un botón de módulo con diseño mejorado"""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        
        button = ctk.CTkButton(
            button_frame,
            text=f"{module['emoji']}\n{module['text']}\n\n{module['description']}",
            command=module['command'],
            height=150,
            font=("Arial", 16, "bold"),
            fg_color=module['color'],
            hover_color=self.darken_color(module['color']),
            text_color="white",
            corner_radius=15
        )
        button.pack(fill="both", expand=True)

    def darken_color(self, color):
        """Oscurecer un color para el efecto hover"""
        # Implementación simple para oscurecer colores hex
        if color.startswith('#'):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            r = max(0, r - 30)
            g = max(0, g - 30)
            b = max(0, b - 30)
            return f'#{r:02x}{g:02x}{b:02x}'
        return color

    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 1400) // 2
        y = (screen_height - 900) // 2
        self.geometry(f'1400x900+{x}+{y}')

    def gestion_nna(self):
        """Abrir gestión de NNA"""
        try:
            # Importar dentro del método para evitar problemas de importación circular
            import importlib
            import sys
            import os
            
            # Agregar el directorio de vistas al path
            views_dir = os.path.join(os.path.dirname(__file__), 'views')
            if views_dir not in sys.path:
                sys.path.append(views_dir)
            
            # Intentar importar dinámicamente
            from views.funcion_vista_nna import main as nna_main
            nna_main()
        except ImportError as e:
            messagebox.showwarning("⚠️ Módulo No Disponible", 
                                f"El módulo de Gestión de NNA no está disponible.\n\nError: {str(e)}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al abrir el módulo: {str(e)}")
    
    def gestion_familiares(self):
        """Abrir gestión de Familiares"""
        try:
            # Importar dentro del método
            import sys
            import os
            
            views_dir = os.path.join(os.path.dirname(__file__), 'views')
            if views_dir not in sys.path:
                sys.path.append(views_dir)
                
            from views.funcion_vista_fami import main as fami_main
            # Crear una nueva ventana para familiares
            fami_main()
        except ImportError as e:
            messagebox.showwarning("⚠️ Módulo No Disponible", 
                                f"El módulo de Gestión de Familiares no está disponible.\n\nError: {str(e)}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al abrir el módulo: {str(e)}")
    
    def gestion_ue(self):
        """Abrir gestión de Unidades Educativas"""
        try:
            import sys
            import os
            
            views_dir = os.path.join(os.path.dirname(__file__), 'views')
            if views_dir not in sys.path:
                sys.path.append(views_dir)
                
            from views.funcion_vista_ue import main as ue_main
            ue_main()
        except ImportError as e:
            messagebox.showwarning("⚠️ Módulo No Disponible", 
                                f"El módulo de Unidades Educativas no está disponible.\n\nError: {str(e)}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al abrir el módulo: {str(e)}")
    
    def gestion_matriculas(self):
        """Abrir gestión de Matrículas"""
        try:
            import sys
            import os
            
            views_dir = os.path.join(os.path.dirname(__file__), 'views')
            if views_dir not in sys.path:
                sys.path.append(views_dir)
                
            from views.funcion_vista_matricula import main as matricula_main
            matricula_main()
        except ImportError as e:
            messagebox.showwarning("⚠️ Módulo No Disponible", 
                                f"El módulo de Matrículas no está disponible.\n\nError: {str(e)}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al abrir el módulo: {str(e)}")
    
    def gestion_articulos(self):
        """Abrir gestión de Artículos"""
        try:
            import sys
            import os
            
            views_dir = os.path.join(os.path.dirname(__file__), 'views')
            if views_dir not in sys.path:
                sys.path.append(views_dir)
                
            from views.funcion_vista_art import main as art_main
            art_main()
        except ImportError as e:
            messagebox.showwarning("⚠️ Módulo No Disponible", 
                                f"El módulo de Artículos no está disponible.\n\nError: {str(e)}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al abrir el módulo: {str(e)}")
    
    def gestion_personal(self):
        """Abrir gestión de Personal"""
        try:
            import sys
            import os
            
            views_dir = os.path.join(os.path.dirname(__file__), 'views')
            if views_dir not in sys.path:
                sys.path.append(views_dir)
                
            from views.funcion_vista_personal import PersonalVista
            # PersonalVista crea su propia ventana Tk()
            personal_window = PersonalVista()
        except ImportError as e:
            messagebox.showwarning("⚠️ Módulo No Disponible", 
                                f"El módulo de Personal no está disponible.\n\nError: {str(e)}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al abrir el módulo: {str(e)}")
            
    def seguimiento_expedientes(self):
        """Abrir módulo de Seguimiento de Expedientes"""
        try:
            # Importa y lanza la función main del archivo de vista.
            # Se asume que funcion_vista_seguimiento_expedientes.py está en una ruta de Python accesible.
            from funcion_vista_seguimiento_expedientes import main as seguimiento_main
            seguimiento_main()
        except ImportError as e:
            messagebox.showwarning("⚠️ Módulo No Disponible", f"El módulo de Seguimiento de Expedientes no está disponible.\n\nError: {str(e)}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al abrir el módulo: {str(e)}")

    def configuracion(self):
        """Abrir módulo de Configuración (como ventana Toplevel)"""
        try:
            # La vista de configuración se abre en una nueva ventana Toplevel
            from configuracion_view import ConfiguracionView
            
            config_window = ctk.CTkToplevel(self)
            # Inicializa la vista de configuración
            ConfiguracionView(config_window)
            
            config_window.protocol("WM_DELETE_WINDOW", config_window.destroy)
            config_window.focus()
            config_window.grab_set() # Convierte la ventana en modal
        except ImportError as e:
            messagebox.showwarning("⚠️ Módulo No Disponible", f"El módulo de Configuración no está disponible.\n\nError: {str(e)}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al abrir el módulo: {str(e)}")

    def reportes(self):
        """Abrir módulo de Reportes (como ventana Toplevel)"""
        try:
            # La vista de reportes se abre en una nueva ventana Toplevel
            from reportes_view import ReportesView
            
            reportes_window = ctk.CTkToplevel(self)
            # Inicializa la vista de reportes
            ReportesView(reportes_window) 
            
            reportes_window.protocol("WM_DELETE_WINDOW", reportes_window.destroy)
            reportes_window.focus()
            reportes_window.grab_set() # Convierte la ventana en modal
        except ImportError as e:
            messagebox.showwarning("⚠️ Módulo No Disponible", f"El módulo de Reportes no está disponible.\n\nError: {str(e)}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al abrir el módulo: {str(e)}")
    
    def mostrar_ayuda(self):
        """Mostrar información de ayuda del sistema"""
        ayuda_texto = """
🏛️ SISTEMA DE GESTIÓN LOPNNA
Consejo de Protección de Niños, Niñas y Adolescentes
📍 Municipio Carrizal

📋 MÓDULOS DISPONIBLES:

👦 Gestión de NNA: Administrar información de Niños, Niñas y Adolescentes
👨‍👩‍👧‍👦 Gestión de Familiares: Gestionar datos de familiares y tutores
🏫 Gestión de UE: Administrar Unidades Educativas
📚 Gestión de Matrículas: Controlar matrículas educativas
📦 Gestión de Artículos: Administrar artículos del sistema
👥 Gestión de Personal: Gestionar usuarios del sistema

🎯 INSTRUCCIONES:
• Para usar cada módulo, haga clic en el botón correspondiente
• Cada módulo se abre en una ventana independiente
• Puede tener múltiples módulos abiertos simultáneamente

📞 CONTACTOS:
• 📧 Soporte técnico: soporte@cpnnacarrizal.gob.ve
• 📞 Teléfono: (0212) 123-4567
• 🏢 Dirección: Av. Principal, Carrizal, Edo. Miranda

🛡️ Protegiendo los derechos de la niñez y adolescencia venezolana
        """
        messagebox.showinfo("❓ Ayuda del Sistema", ayuda_texto)
    
    def on_closing(self):
        """Manejar el cierre de la aplicación"""
        if messagebox.askyesno("🚪 Salir del Sistema", "¿Está seguro de que desea salir del sistema?"):
            # Limpiar y destruir
            self.cleanup()
            self.destroy()
            sys.exit(0)

    def cleanup(self):
        """Limpiar recursos antes de cerrar"""
        try:
            # Cancelar todos los eventos pendientes
            for after_id in self.tk.eval('after info').split():
                self.after_cancel(after_id)
        except:
            pass

def iniciar_sistema():
    """Función para iniciar el sistema completo"""
    try:
        # Primero intentar con login
        from funcion_login import LoginApp
        login_app = LoginApp()
        login_app.run()
    except ImportError:
        # Si no hay login, ir directamente al menú principal
        app = MenuApp()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo iniciar el sistema: {str(e)}")
        sys.exit(1)

def main():
    """Función principal alternativa"""
    app = MenuApp()
    app.mainloop()

if __name__ == "__main__":
    # Opción 1: Con login
    iniciar_sistema()
