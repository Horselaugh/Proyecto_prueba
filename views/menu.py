import customtkinter as ctk
from tkinter import messagebox
import sys

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

        # Definir módulos con emojis y colores
        modules = [
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
        ]

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
            text="🚪 Cerrar Sesión",
            command=self.cerrar_sesion,
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
            from funcion_vista_nna import main
            main()
        except ImportError as e:
            messagebox.showerror("❌ Error", f"No se pudo abrir el módulo NNA: {str(e)}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error inesperado: {str(e)}")
    
    def gestion_familiares(self):
        """Abrir gestión de Familiares"""
        try:
            from funcion_vista_fami import main
            main()
        except ImportError as e:
            messagebox.showerror("❌ Error", f"No se pudo abrir el módulo Familiares: {str(e)}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error inesperado: {str(e)}")
    
    def gestion_ue(self):
        """Abrir gestión de Unidades Educativas"""
        try:
            from funcion_vista_ue import main
            main()
        except ImportError as e:
            messagebox.showerror("❌ Error", f"No se pudo abrir el módulo UE: {str(e)}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error inesperado: {str(e)}")
    
    def gestion_matriculas(self):
        """Abrir gestión de Matrículas"""
        try:
            from funcion_vista_matricula import main
            main()
        except ImportError as e:
            messagebox.showerror("❌ Error", f"No se pudo abrir el módulo Matrículas: {str(e)}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error inesperado: {str(e)}")
    
    def gestion_articulos(self):
        """Abrir gestión de Artículos"""
        try:
            from funcion_vista_art import main
            main()
        except ImportError as e:
            messagebox.showerror("❌ Error", f"No se pudo abrir el módulo Artículos: {str(e)}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error inesperado: {str(e)}")
    
    def gestion_personal(self):
        """Abrir gestión de Personal"""
        try:
            from funcion_vista_personal import PersonalVista
            # PersonalVista crea su propia ventana Tk()
            PersonalVista()
        except ImportError as e:
            messagebox.showerror("❌ Error", f"No se pudo abrir el módulo Personal: {str(e)}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error inesperado: {str(e)}")
    
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
    
    def cerrar_sesion(self):
        """Cerrar sesión y volver al login"""
        if messagebox.askyesno("🚪 Cerrar Sesión", "¿Está seguro de que desea cerrar sesión?"):
            self.destroy()
            # Volver al login
            try:
                from views.funcion_login import LoginApp
                login_app = LoginApp()
                login_app.run()
            except ImportError:
                # Si no se puede volver al login, cerrar completamente
                sys.exit(0)

if __name__ == "__main__":
    # Si se ejecuta menu.py directamente, iniciar el login primero
    try:
        from funcion_login import LoginApp
        login_app = LoginApp()
        login_app.run()
    except ImportError:
        # Si no existe el login, iniciar el menú directamente
        app = MenuApp()
        app.mainloop()