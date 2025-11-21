import customtkinter as ctk
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.articulo_model import ArticuloModelo

class ArticuloVista:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("📦 Gestión de Artículos LOPNNA")
        self.root.geometry("1200x800")
        self.root.configure(fg_color="#2e2e2e")
        
        # Variables de control
        self.buscar_var = ctk.StringVar()
        self.codigo_var = ctk.StringVar()
        self.articulo_var = ctk.StringVar()
        self.descripcion_var = ctk.StringVar()
        
        # Inicializar eventos con funciones vacías para evitar el error
        self.eventos = {
            "agregar_articulo": lambda: None,
            "buscar_articulo": lambda: None,
            "modificar_articulo": lambda: None,
            "eliminar_articulo": lambda: None
        }
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=10)

        # Título
        title_label = ctk.CTkLabel(
            main_frame,
            text="📦 GESTIÓN DE ARTÍCULOS LOPNNA",
            font=("Arial", 28, "bold"),
            text_color="#1abc9c"
        )
        title_label.pack(pady=(0, 30))

        # Frame de búsqueda
        search_frame = ctk.CTkFrame(main_frame)
        search_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            search_frame,
            text="🔍 Buscar Artículo:",
            font=("Arial", 16, "bold")
        ).pack(side="left", padx=20, pady=15)

        search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.buscar_var,
            placeholder_text="Ingrese código o nombre del artículo...",
            height=45,
            font=("Arial", 14)
        )
        search_entry.pack(side="left", fill="x", expand=True, padx=10, pady=15)

        search_btn = ctk.CTkButton(
            search_frame,
            text="🔍 Buscar",
            command=lambda: self.eventos["buscar_articulo"](),
            height=45,
            font=("Arial", 14),
            fg_color="#3498db"
        )
        search_btn.pack(side="right", padx=20, pady=15)

        # Frame de formulario
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(fill="x", pady=20)

        # Campos del formulario
        campos = [
            ("📋 Código:", self.codigo_var, "Ej: ART-001"),
            ("📝 Artículo:", self.articulo_var, "Ej: Cuadernos escolares"),
            ("📄 Descripción:", self.descripcion_var, "Ej: Cuadernos tamaño carta, 100 hojas")
        ]

        for i, (label, var, placeholder) in enumerate(campos):
            ctk.CTkLabel(form_frame, text=label, font=("Arial", 14)).grid(row=i, column=0, padx=20, pady=15, sticky="e")
            entry = ctk.CTkEntry(
                form_frame,
                textvariable=var,
                placeholder_text=placeholder,
                height=45,
                font=("Arial", 14)
            )
            entry.grid(row=i, column=1, padx=20, pady=15, sticky="ew")

        # Para la descripción usar un Textbox más grande
        form_frame.grid_rowconfigure(2, weight=1)
        desc_frame = ctk.CTkFrame(form_frame)
        desc_frame.grid(row=2, column=1, padx=20, pady=15, sticky="nsew")
        
        self.desc_textbox = ctk.CTkTextbox(desc_frame, height=100, font=("Arial", 14))
        self.desc_textbox.pack(fill="both", expand=True)

        form_frame.grid_columnconfigure(1, weight=1)

        # Frame de botones
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=10)

        botones = [
            ("➕ Agregar", lambda: self.eventos["agregar_articulo"](), "#27ae60"),
            ("✏️ Modificar", lambda: self.eventos["modificar_articulo"](), "#f39c12"),
            ("🗑️ Eliminar", lambda: self.eventos["eliminar_articulo"](), "#e74c3c"),
            ("🧹 Limpiar", self.limpiar_entradas, "#7f8c8d")
        ]

        for texto, comando, color in botones:
            btn = ctk.CTkButton(
                buttons_frame,
                text=texto,
                command=comando,
                height=50,
                font=("Arial", 14, "bold"),
                fg_color=color,
                hover_color=color
            )
            btn.pack(side="left", expand=True, padx=10)

    def establecer_eventos(self, **kwargs): 
        self.eventos.update(kwargs)
        
    def mostrar_mensaje(self, mensaje, color="#FFFFFF"): 
        # Crear ventana de mensaje
        msg_window = ctk.CTkToplevel(self.root)
        msg_window.title("💬 Mensaje del Sistema")
        msg_window.geometry("500x200")
        msg_window.configure(fg_color="#2e2e2e")
        
        # Centrar ventana
        msg_window.transient(self.root)
        msg_window.grab_set()
        
        ctk.CTkLabel(
            msg_window,
            text=mensaje,
            font=("Arial", 14),
            text_color=color
        ).pack(expand=True, fill="both", padx=30, pady=10)
        
        ctk.CTkButton(
            msg_window,
            text="✅ Aceptar",
            command=msg_window.destroy,
            fg_color="#3498db"
        ).pack(pady=10)
        
    def obtener_valores(self): 
        return {
            "termino_busqueda": self.buscar_var.get(),
            "codigo": self.codigo_var.get(),
            "articulo": self.articulo_var.get(),
            "descripcion": self.desc_textbox.get("1.0", "end-1c")
        }
        
    def establecer_valores(self, **kwargs): 
        if "codigo" in kwargs:
            self.codigo_var.set(kwargs["codigo"])
        if "articulo" in kwargs:
            self.articulo_var.set(kwargs["articulo"])
        if "descripcion" in kwargs:
            self.desc_textbox.delete("1.0", "end")
            self.desc_textbox.insert("1.0", kwargs["descripcion"])
        
    def limpiar_entradas(self): 
        self.buscar_var.set("")
        self.codigo_var.set("")
        self.articulo_var.set("")
        self.desc_textbox.delete("1.0", "end")
        
    def mostrar_literales(self, literales): 
        pass
        
    def run(self):
        self.root.mainloop()

class ArticuloControlador:
    """
    Controlador que maneja la interacción entre el Modelo y la Vista.
    Contiene la lógica de la aplicación.
    """
    def __init__(self, modelo: ArticuloModelo, vista: ArticuloVista):
        self.modelo = modelo
        self.vista = vista
        
        self.articulo_original_id = None 
        
        self.vista.establecer_eventos(
            agregar_articulo=self.agregar_articulo,
            buscar_articulo=self.leer_articulo,
            modificar_articulo=self.modificar_articulo,
            eliminar_articulo=self.eliminar_articulo
        )
        
        self.vista.mostrar_mensaje("¡📦 Gestor de Artículos LOPNNA listo! 🚀", color="#3CB371")
        self.vista.run()

    def _validar_campos_requeridos(self, data: dict) -> bool:
        """Verifica que los campos estén llenos."""
        if not data["codigo"]:
            self.vista.mostrar_mensaje("❌ Error: El código del artículo es obligatorio.", color="#FF5733")
            return False
        if not data["articulo"]:
            self.vista.mostrar_mensaje("❌ Error: El nombre del artículo es obligatorio.", color="#FF5733")
            return False
        if not data["descripcion"]:
            self.vista.mostrar_mensaje("❌ Error: La descripción del artículo no puede estar vacía.", color="#FF5733")
            return False
        return True

    def agregar_articulo(self):
        """Lógica para crear un nuevo artículo."""
        data = self.vista.obtener_valores()
        
        if not self._validar_campos_requeridos(data):
            return
            
        self.articulo_original_id = None 

        # Insertar Artículo
        articulo_id = self.modelo.insertar_articulo(
            data["codigo"], 
            data["articulo"], 
            data["descripcion"]
        )

        if articulo_id:
            self.vista.mostrar_mensaje(f"✅ Artículo '{data['articulo']}' creado y guardado correctamente. 📦", color="#3CB371")
            self.vista.limpiar_entradas()
        else:
            self.vista.mostrar_mensaje(f"❌ Error: El código {data['codigo']} ya existe.", color="#FF5733")

    def leer_articulo(self):
        """
        Lógica para buscar y mostrar un artículo.
        """
        termino = self.vista.obtener_valores()["termino_busqueda"]
        
        if not termino:
            self.vista.mostrar_mensaje("⚠️ Advertencia: Ingrese un código o palabra clave para buscar.", color="#FFBF00")
            self.articulo_original_id = None
            return

        articulo_encontrado = self.modelo.buscar_articulo(termino)
        
        if articulo_encontrado:
            self.articulo_original_id = articulo_encontrado["id"]
            
            self.vista.establecer_valores(
                codigo=articulo_encontrado["codigo"],
                articulo=articulo_encontrado["articulo"],
                descripcion=articulo_encontrado["descripcion"]
            )
            self.vista.mostrar_mensaje(
                f"🔍 Artículo '{articulo_encontrado['articulo']}' encontrado y cargado. ✅", 
                color="#219EBC"
            )
        else:
            self.vista.limpiar_entradas()
            self.vista.buscar_var.set(termino)
            self.articulo_original_id = None
            self.vista.mostrar_mensaje(f"❌ Artículo o término '{termino}' no encontrado.", color="#FF5733")

    def modificar_articulo(self):
        """Lógica para modificar un artículo existente."""
        data = self.vista.obtener_valores()
        
        if not self._validar_campos_requeridos(data):
            return
            
        if not self.articulo_original_id:
            self.vista.mostrar_mensaje("⚠️ Advertencia: Busque y cargue un artículo antes de intentar modificar.", color="#FFBF00")
            return
            
        # Modificar Artículo
        if self.modelo.modificar_articulo(
            self.articulo_original_id,
            data["codigo"],
            data["articulo"],
            data["descripcion"]
        ):
            self.vista.mostrar_mensaje(f"✏️ Artículo '{data['articulo']}' modificado con éxito. ✅", color="#FFA500")
            self.vista.limpiar_entradas()
            # Actualizar referencia si el código cambió
            articulo_actualizado = self.modelo.buscar_articulo(data["codigo"])
            if articulo_actualizado:
                self.articulo_original_id = articulo_actualizado["id"]
        else:
            self.vista.mostrar_mensaje("❌ Error: Falló la modificación. Revise el código o la consola.", color="#FF5733")

    def eliminar_articulo(self):
        """Lógica para eliminar un artículo existente."""
        data = self.vista.obtener_valores()
        
        if not self.articulo_original_id:
            self.vista.mostrar_mensaje("❌ Error: Debe cargar un artículo antes de eliminarlo.", color="#FF5733")
            return
            
        # Intentar eliminar en el Modelo
        if self.modelo.eliminar_articulo(self.articulo_original_id):
            self.vista.mostrar_mensaje(f"🗑️ Artículo eliminado con éxito. ✅", color="#B80000")
            self.vista.limpiar_entradas()
            self.articulo_original_id = None
        else:
            self.vista.mostrar_mensaje(f"❌ Error: El artículo no fue encontrado.", color="#FF5733")

# Función principal para ejecutar el módulo
def main():
    modelo = ArticuloModelo()
    vista = ArticuloVista()
    controlador = ArticuloControlador(modelo, vista)

if __name__ == "__main__":
    main()